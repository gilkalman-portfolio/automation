#!/usr/bin/env python3
"""
automated_test_runner.py
========================
Automated test runner agent for the Playwright + pytest automation project.

What it does every cycle:
  1. Runs pytest and captures structured results (JSON + JUnit XML)
  2. If failures are found → spawns a Claude Agent to analyze and fix them
  3. Re-runs only the failed tests after fixes
  4. Generates a detailed Markdown report in reports/

Usage:
  # Single run now:
  python automated_test_runner.py

  # Smoke tests only:
  python automated_test_runner.py -m smoke

  # Scheduled run every 24 hours:
  python automated_test_runner.py --schedule

  # Custom interval (e.g. every 6 hours):
  python automated_test_runner.py --schedule --interval-hours 6
"""

from __future__ import annotations

import anyio
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.resolve()
REPORTS_DIR = PROJECT_ROOT / "reports"
TEST_RUNS_DIR = PROJECT_ROOT / "test_runs"

# System prompt that gives the agent full project context
AGENT_SYSTEM_PROMPT = """You are an automated test-maintenance engineer for a Playwright + pytest project.

## Project layout
- test_cases/          → all test files (test_*.py)
- page_objects/        → Page Object Model classes
- workflows/           → high-level workflow helpers (web_workflow.py, api_workflow.py)
- utilities/           → config_loader.py, logger.py, common_ops.py
- configuration/data.xml → main config (env, base_url, browsers, headless, etc.)
- conftest.py (in test_cases/) → fixtures, browser setup

## Rules you MUST follow
1. Only modify: test_cases/, page_objects/, workflows/, configuration/data.xml, utilities/config_loader.py
2. Never hard-code URLs or credentials — always read from data.xml via config_loader
3. Never use time.sleep() — use Playwright's built-in waits/expects
4. Prefer stable selectors: data-testid, ARIA role, visible text; avoid fragile CSS/XPath
5. Keep fixes minimal — do not refactor or rename working code
6. Do NOT change pytest.ini markers

## Workflow
1. Read the failing test file(s) to understand the test logic
2. Read the related page object(s) and workflow(s) for full context
3. Identify the root cause (wrong selector, bad assertion, import error, etc.)
4. Apply the smallest possible fix
5. End your response with a FIXES_SUMMARY block (see format below)

## FIXES_SUMMARY format (required at end of response)
```
FIXES_SUMMARY:
- tests/path/test_file.py::ClassName::test_name: <one-line description of the fix>
- tests/path/test_file.py::test_name: <one-line description of the fix>
```
"""


# ---------------------------------------------------------------------------
# Step 1 — Run pytest
# ---------------------------------------------------------------------------

def run_pytest(output_dir: Path, nodeids: list[str] | None = None, marker: str | None = None) -> dict:
    """
    Run pytest and return the parsed JSON report dict.
    Extra keys injected: _stdout, _stderr, _returncode.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    json_report = output_dir / "report.json"
    junit_xml = output_dir / "junit.xml"

    cmd = [
        sys.executable, "-m", "pytest",
        "--json-report", f"--json-report-file={json_report}",
        f"--junitxml={junit_xml}",
        "-v", "--tb=short",
        # Keep output concise for CI-style logs
        "-q",
    ]

    if marker:
        cmd.extend(["-m", marker])

    if nodeids:
        cmd.extend(nodeids)

    env = os.environ.copy()
    env["TEST_OUTPUT_DIR"] = str(output_dir)

    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )

    report: dict = {}
    if json_report.exists():
        try:
            with open(json_report, encoding="utf-8") as fh:
                report = json.load(fh)
        except json.JSONDecodeError as exc:
            print(f"  ⚠️  Could not parse JSON report: {exc}")

    report["_stdout"] = result.stdout
    report["_stderr"] = result.stderr
    report["_returncode"] = result.returncode

    return report


# ---------------------------------------------------------------------------
# Step 2 — Claude Agent fix
# ---------------------------------------------------------------------------

def _format_failure(test: dict) -> str:
    """Format a single test failure for the agent prompt."""
    node = test.get("nodeid", "unknown")
    call = test.get("call", {})
    longrepr = call.get("longrepr", "") or ""
    # Truncate very long tracebacks so the prompt stays focused
    if len(longrepr) > 1500:
        longrepr = longrepr[:1500] + "\n... (truncated)"
    return f"### `{node}`\n```\n{longrepr}\n```"


async def run_fix_agent(failures: list[dict]) -> str:
    """
    Spawn a Claude Agent SDK agent to analyse and fix the failing tests.
    Returns the agent's final result text (includes FIXES_SUMMARY).
    """
    failure_blocks = "\n\n".join(_format_failure(t) for t in failures)

    prompt = f"""The following {len(failures)} test(s) are currently failing.
Analyse each failure, identify the root cause, and apply the minimal fix.

---

{failure_blocks}

---

Start by reading the relevant test file(s), page objects, and workflow helpers.
Then apply your fixes and finish with a FIXES_SUMMARY block.
"""

    result_text = ""
    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            cwd=str(PROJECT_ROOT),
            allowed_tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"],
            permission_mode="acceptEdits",
            model="claude-opus-4-6",
            thinking={"type": "adaptive"},
            system_prompt=AGENT_SYSTEM_PROMPT,
            max_turns=50,
        ),
    ):
        if isinstance(message, ResultMessage):
            result_text = message.result

    return result_text


# ---------------------------------------------------------------------------
# Step 3 — Generate Markdown report
# ---------------------------------------------------------------------------

def _outcomes(report: dict) -> tuple[int, int, int, int]:
    """Return (passed, failed, error, skipped) counts from a pytest JSON report."""
    tests = report.get("tests", [])
    passed = sum(1 for t in tests if t.get("outcome") == "passed")
    failed = sum(1 for t in tests if t.get("outcome") == "failed")
    error = sum(1 for t in tests if t.get("outcome") == "error")
    skipped = sum(1 for t in tests if t.get("outcome") == "skipped")
    return passed, failed, error, skipped


def generate_report(
    run_id: str,
    initial_report: dict,
    final_report: dict,
    fix_summary: str,
    run_dir: Path,
) -> Path:
    """Write a Markdown report and return its path."""

    i_pass, i_fail, i_err, i_skip = _outcomes(initial_report)
    f_pass, f_fail, f_err, f_skip = _outcomes(final_report)

    initial_failures = [
        t for t in initial_report.get("tests", [])
        if t.get("outcome") in ("failed", "error")
    ]
    final_failures = [
        t for t in final_report.get("tests", [])
        if t.get("outcome") in ("failed", "error")
    ]
    final_failure_ids = {t["nodeid"] for t in final_failures}

    fixed_count = len(initial_failures) - len(final_failures)
    still_failing = len(final_failures)

    if still_failing == 0:
        status_badge = "✅ ALL PASSING"
    else:
        status_badge = f"⚠️ {still_failing} STILL FAILING"

    duration = final_report.get("duration", initial_report.get("duration", 0))

    lines: list[str] = [
        f"# Automated Test Report — {run_id}",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Status:** {status_badge}  ",
        f"**Duration:** {duration:.1f}s",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Before | After |",
        "|--------|--------|-------|",
        f"| ✅ Passed  | {i_pass} | {f_pass} |",
        f"| ❌ Failed  | {i_fail} | {f_fail} |",
        f"| 💥 Error   | {i_err}  | {f_err}  |",
        f"| ⏭️ Skipped | {i_skip} | {f_skip} |",
        f"| 🔧 Fixed   | —      | {fixed_count} |",
        "",
    ]

    # ── Initial failures detail ──────────────────────────────────────────
    if initial_failures:
        lines += [
            "---",
            "",
            f"## Initial Failures ({len(initial_failures)})",
            "",
        ]
        for t in initial_failures:
            was_fixed = t["nodeid"] not in final_failure_ids
            badge = "FIXED ✅" if was_fixed else "STILL FAILING ❌"
            lines += [f"### `{t['nodeid']}` — {badge}", ""]

            longrepr = (t.get("call") or {}).get("longrepr", "")
            if longrepr:
                if len(longrepr) > 1200:
                    longrepr = longrepr[:1200] + "\n... (truncated)"
                lines += ["```", longrepr, "```", ""]

    # ── Agent fix summary ────────────────────────────────────────────────
    if fix_summary:
        lines += [
            "---",
            "",
            "## Agent Fix Summary",
            "",
            fix_summary.strip(),
            "",
        ]

    # ── Remaining failures ───────────────────────────────────────────────
    if final_failures:
        lines += [
            "---",
            "",
            f"## Remaining Failures ({len(final_failures)})",
            "",
        ]
        for t in final_failures:
            lines += [f"### `{t['nodeid']}`", ""]
            longrepr = (t.get("call") or {}).get("longrepr", "")
            if longrepr:
                if len(longrepr) > 1000:
                    longrepr = longrepr[:1000] + "\n... (truncated)"
                lines += ["```", longrepr, "```", ""]

    # ── Artifacts ────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Artifacts",
        "",
        f"- Run directory: `{run_dir}`",
        f"- Initial JSON report: `{run_dir / 'initial' / 'report.json'}`",
        f"- Final JSON report:   `{run_dir / 'after_fix' / 'report.json'}`",
        f"- Screenshots: `{run_dir / 'after_fix' / 'screenshots/'}`",
        "",
    ]

    report_text = "\n".join(lines)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"report_{run_id}.md"
    report_path.write_text(report_text, encoding="utf-8")
    return report_path


# ---------------------------------------------------------------------------
# Main cycle
# ---------------------------------------------------------------------------

async def run_cycle(marker: str | None = None) -> Path:
    """
    Execute one full cycle:
      run → (fix if needed) → re-run → report
    Returns the path to the generated Markdown report.
    """
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = TEST_RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  🚀  Test Run: {run_id}" + (f"  [-m {marker}]" if marker else ""))
    print(sep)

    # ── Step 1: initial test run ─────────────────────────────────────────
    print("\n📋 Step 1/3 — Running tests …")
    initial_report = run_pytest(run_dir / "initial", marker=marker)

    initial_failures = [
        t for t in initial_report.get("tests", [])
        if t.get("outcome") in ("failed", "error")
    ]
    total = len(initial_report.get("tests", []))
    i_pass = sum(1 for t in initial_report.get("tests", []) if t.get("outcome") == "passed")
    print(f"   → {i_pass}/{total} passed, {len(initial_failures)} failed/errored")

    fix_summary = ""
    final_report = initial_report  # default: no re-run needed

    # ── Step 2: fix with Claude agent (only if there are failures) ────────
    if initial_failures:
        print(f"\n🔧 Step 2/3 — Fixing {len(initial_failures)} failure(s) with Claude agent …")
        fix_summary = await run_fix_agent(initial_failures)

        # ── Step 3: re-run failed tests only ─────────────────────────────
        print("\n🔄 Step 3/3 — Re-running previously failing tests …")
        failed_nodeids = [t["nodeid"] for t in initial_failures]
        final_report = run_pytest(
            run_dir / "after_fix",
            nodeids=failed_nodeids,
        )
        final_failures = [
            t for t in final_report.get("tests", [])
            if t.get("outcome") in ("failed", "error")
        ]
        fixed = len(initial_failures) - len(final_failures)
        print(f"   → Fixed: {fixed}/{len(initial_failures)},  still failing: {len(final_failures)}")
    else:
        print("\n✅ All tests passed — nothing to fix")
        # Mirror structure so report generation always works
        (run_dir / "after_fix").mkdir(parents=True, exist_ok=True)

    # ── Step 4: generate report ──────────────────────────────────────────
    print("\n📊 Generating report …")
    report_path = generate_report(run_id, initial_report, final_report, fix_summary, run_dir)
    print(f"   → {report_path}")

    return report_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automated test runner with Claude AI fix agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run on a recurring schedule (blocking)",
    )
    parser.add_argument(
        "--interval-hours",
        type=float,
        default=24.0,
        metavar="N",
        help="Hours between scheduled runs (default: 24)",
    )
    parser.add_argument(
        "-m", "--marker",
        default=None,
        metavar="MARK",
        help="Pytest marker filter, e.g. smoke, regression",
    )
    args = parser.parse_args()

    async def _run() -> Path:
        return await run_cycle(marker=args.marker)

    if args.schedule:
        interval_sec = int(args.interval_hours * 3600)
        print(f"⏰  Scheduler active — interval: {args.interval_hours}h  (Ctrl-C to stop)")
        while True:
            try:
                report = anyio.run(_run)
                next_run = datetime.fromtimestamp(time.time() + interval_sec)
                print(f"\n✅  Cycle complete — next run at {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Report: {report}")
            except KeyboardInterrupt:
                print("\n🛑  Scheduler stopped")
                sys.exit(0)
            except Exception as exc:
                print(f"\n❌  Cycle error: {exc}")
            time.sleep(interval_sec)
    else:
        report = anyio.run(_run)
        print(f"\n✅  Done!  Report → {report}")


if __name__ == "__main__":
    main()
