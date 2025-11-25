from __future__ import annotations

from typing import Optional, Dict, Any
from pathlib import Path
import subprocess
import shlex

from mcp.server.fastmcp import FastMCP

# "The name that will appear in Claude in the tool list"
mcp = FastMCP("pytest-runner")


@mcp.tool()
def run_pytest(
    marker: Optional[str] = None,
    test_path: str = "test_cases",
    extra_args: str = "",
) -> Dict[str, Any]:
    """
   Args:
    marker:
        An expression for pytest -m, for example:
        "smoke" or "regression and not slow".
    test_path:
        The path (relative to the project root) from which to run tests.
        Default: "test_cases".
    extra_args:
        Additional flags for pytest, for example:
        "-vv --maxfail=1".
    """
    # "Project root – the directory where this file is located"
    project_root = Path(__file__).resolve().parent

    cmd = ["pytest", test_path]

    if marker:
        cmd.extend(["-m", marker])

    if extra_args:
        cmd.extend(shlex.split(extra_args))

    # "Running pytest as a subprocess"
    proc = subprocess.run(
        cmd,
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )

    # "Limit output length so as not to overload the model."
    max_len = 8000
    stdout_trimmed = (
        proc.stdout if len(proc.stdout) <= max_len else proc.stdout[-max_len:]
    )
    stderr_trimmed = (
        proc.stderr if len(proc.stderr) <= max_len else proc.stderr[-max_len:]
    )

    return {
        "command": " ".join(cmd),
        "exit_code": proc.returncode,
        "stdout": stdout_trimmed,
        "stderr": stderr_trimmed,
    }


def main() -> None:
    # "Running the server in STDIO mode – what Claude and MCP expect"
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
