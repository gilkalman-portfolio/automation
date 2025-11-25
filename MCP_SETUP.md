# MCP-ready QA Project — Quick Start

This project layout is ready for AI + MCP orchestration.

## 1) Files included
- `tests/conftest.py` — MCP-friendly fixtures (TEST_OUTPUT_DIR, trace export on failure, CLI overrides).
- `utilities/config_loader.py` — Loads `configuration/data.xml` + ENV overrides.
- `configuration/data.xml` — Central runtime config (env, baseUrl, browsers/devices, trace/video/screenshot).
- `mcp.config.json` — Example MCP client configuration (allowlisted commands, env vars, paths).
- `requirements.txt` — All dependencies, including JSON/JUnit reporters.

## 2) Install
```bash
pip install -r requirements.txt
playwright install
```

## 3) Local runs
```bash
# Use XML defaults
pytest

# Single test
pytest tests/test_example.py::test_open_example

# With artifacts in a specific folder
set TEST_OUTPUT_DIR=.\run1
pytest --alluredir %TEST_OUTPUT_DIR%\allure-results --junitxml %TEST_OUTPUT_DIR%\reports\junit.xml --json-report --json-report-file %TEST_OUTPUT_DIR%\reports\report.json
```

## 4) What MCP should do
- Set `TEST_OUTPUT_DIR` per run (e.g., `/tmp/run-123`).
- Call pytest with reporters enabled:
  ```bash
  pytest -q --alluredir $TEST_OUTPUT_DIR/allure-results --junitxml $TEST_OUTPUT_DIR/reports/junit.xml --json-report --json-report-file $TEST_OUTPUT_DIR/reports/report.json
  ```
- Optionally add:
  - `-n {workers}` for parallel
  - `-m "smoke or regression"` for tag selection
  - `--browsers=chromium,firefox --devices=desktop,"Pixel 7"` to override XML

## 5) Artifacts collected by MCP
- `$TEST_OUTPUT_DIR/reports/junit.xml` — JUnit XML
- `$TEST_OUTPUT_DIR/reports/report.json` — JSON report
- `$TEST_OUTPUT_DIR/allure-results` — Allure raw results
- `$TEST_OUTPUT_DIR/screenshots` — Screenshots on failure or always (policy)
- `$TEST_OUTPUT_DIR/traces` — Playwright trace zips on failure (when `trace=retain-on-failure`)
- `$TEST_OUTPUT_DIR/videos` — Browser videos (if enabled)

## 6) Where to define MCP
- MCP is configured in your AI client (IDE plugin or orchestrator) — point it at this repository and load `mcp.config.json`.
- Ensure the AI client runs commands only from the allowlist, writes only under allowed folders, and sets ENV as specified.

## 7) Tips
- Keep `data.xml` as the single source of truth for runtime defaults.
- Use CLI/ENV to override per run — especially in CI or MCP-driven runs.
- Consider adding CI jobs that publish Allure reports after each run.
