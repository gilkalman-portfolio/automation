# AI Agent Guide for This Automation Project

This document explains how an AI agent should work with this project
using PyCharm MCP Server + Pytest + Playwright (Python). It defines
rules, workflows, environment setup, and safety boundaries.

------------------------------------------------------------------------

# 1. Technology Stack & Environment

-   Language: **Python 3.14**
-   Frameworks: **Pytest + Playwright (Python bindings)**
-   OS: **Windows**
-   Always work inside a **virtual environment (venv)**.

## Virtual Environment Setup

From the project root:

``` bash
python -m venv venv
.env\Scriptsctivate
pip install -r requirements.flex.txt
python -m playwright install
```

------------------------------------------------------------------------

# 2. Project Structure

Important directories and files:

    tests/                        → All test files live here
    utilities/
        config_loader.py          → Loads XML config + ENV/CLI overrides
    configuration/
        data.xml                  → Main config (env, base URL, browsers, traces, retries…)
    conftest.py                   → Fixtures, browser setup, trace/video/screenshots, TEST_OUTPUT_DIR
    pytest.ini                    → Markers (smoke, regression, sanity), addopts, allure dir
    requirements.flex.txt         → Flexible dependencies for Python 3.14

------------------------------------------------------------------------

# 3. How to Run Tests (Shell via MCP)

Always run commands from the **project root**.

## TEST_OUTPUT_DIR

Before running tests:

``` bash
set TEST_OUTPUT_DIR=run_name_here
```

## Smoke Example

``` bash
set TEST_OUTPUT_DIR=run_smoke_01
pytest -q -m smoke ^
  --alluredir %TEST_OUTPUT_DIR%\allure-results ^
  --junitxml %TEST_OUTPUT_DIR%\reports\junit.xml ^
  --json-report --json-report-file %TEST_OUTPUT_DIR%\reports\report.json
```

## Other Examples

Regression:

``` bash
pytest -q -m regression
```

Sanity:

``` bash
pytest -q -m sanity
```

Specific test:

``` bash
pytest tests/test_login.py::test_valid_login
```

------------------------------------------------------------------------

# 4. Rules for Test Editing

1.  Modify only:
    -   tests/
    -   conftest.py
    -   configuration/data.xml
    -   utilities/config_loader.py (only when necessary)
    -   pytest.ini (markers/addopts only)
2.  **No hard-coded values**:
    -   No direct URLs or browser names
    -   Always use values from data.xml via config_loader
3.  **Markers**:
    -   smoke
    -   regression
    -   sanity
4.  **Selectors**:
    -   Prefer stable: data-testid, role, meaningful text
    -   Avoid fragile CSS/XPath
    -   Never use sleep()
5.  **Failure analysis**:
    -   console logs
    -   junit.xml
    -   json-report
    -   trace/video/screenshots
6.  **Re-run after fixing**:
    -   Only the relevant test subset
    -   Use a new TEST_OUTPUT_DIR

------------------------------------------------------------------------

# 5. Standard AI Workflow

1.  Understand request\
2.  Open relevant files\
3.  Run pytest with correct marker/path\
4.  Analyze report\
5.  Apply minimal fix\
6.  Re-run\
7.  Summarize changes

------------------------------------------------------------------------

# 6. CI/CD Compatibility

-   CI uses the same test suite under tests/
-   CI installs requirements.flex.txt and playwright
-   Tests must be deterministic and stable
-   Avoid flaky behavior or environment-specific assumptions

------------------------------------------------------------------------

# 7. Safety & Boundaries

-   Do not run destructive shell commands

-   Do not delete external files

-   Stay inside the project folder

-   ## Ask clarification when unsure
