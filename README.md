# Automation Testing Framework

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-Latest-orange.svg)](https://pytest.org/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF.svg)](https://github.com/features/actions)

A **production-ready automation framework** with AI-powered test maintenance, scheduled CI runs, and Telegram notifications.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [Automated Test Runner](#automated-test-runner)
- [CI/CD — GitHub Actions](#cicd--github-actions)

---

## Manual & Automation STP
    ## 🔗 Links
    Automation:
- [Live Portfolio Site](https://gilkalman-portfolio.github.io/gil-kalman.github.io/)
    Manual:
- [Live Portfolio Site](https://gilkalman-portfolio.github.io/gil-kalman.github.io/manual,html)
    

## Overview

This project demonstrates **professional-grade automation testing** with:

- **Clean, production-style code** with Page Object Model + Workflows separation
- **XML-based configuration** for flexible, code-free environment management
- **AI Agent** that automatically analyses and fixes failing tests
- **Scheduled CI** via GitHub Actions (runs daily, reports to Telegram)
- **Comprehensive reporting** with Allure + Markdown reports

---

## Key Features

### Dynamic Configuration
- XML-based configuration (`data.xml`) — browser, environment, headless, retries, etc.
- CLI parameter overrides at runtime
- No code changes needed to adapt to different environments

### AI-Powered Test Maintenance
- **Claude Agent SDK** integration (`claude-haiku-4-5`)
- Automatically reads failing tests, identifies root cause, applies minimal fix
- Re-runs only the failed tests after fixing to verify
- Opt-in via `--ai-fix` flag — never runs without explicit permission

### Scheduled CI with Telegram Notifications
- GitHub Actions workflow runs every day at 02:00 UTC
- Manual dispatch available from GitHub UI (with marker filter)
- Sends a summary message + full Markdown report to a Telegram bot

### Clean Architecture
- **Page Objects + Workflows** design pattern
- Centralized page management (`manage_pages.py`)
- Reusable fixtures, utilities, and typed configuration

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.12+ |
| **Test Runner** | Pytest |
| **Browser Automation** | Playwright |
| **Test Design** | Page Objects + Workflows |
| **Config System** | XML (`data.xml`) + `config_loader.py` |
| **Reporting** | Allure + Markdown (`reports/`) |
| **AI Fix Agent** | Claude Agent SDK (`claude-haiku-4-5`) |
| **CI/CD** | GitHub Actions (scheduled + manual dispatch) |
| **Notifications** | Telegram Bot API |

---

## Project Structure

```
automation/
├── automated_test_runner.py     # AI-powered scheduled test runner
│
├── .github/
│   └── workflows/
│       └── scheduled_test_runner.yml  # GitHub Actions — daily + manual
│
├── configuration/
│   └── data.xml                 # Main config (browser, env, headless…)
│
├── utilities/
│   ├── config_loader.py         # Loads & normalizes XML config
│   ├── manage_pages.py          # Central Page Objects manager
│   └── logger.py
│
├── page_objects/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── workflows/
│   ├── web_workflow.py          # UI workflows (login, cart, checkout…)
│   └── api_workflow.py
│
├── test_cases/
│   ├── conftest.py              # Fixtures, browser setup, trace/screenshot
│   ├── test_saucedemo.py        # 20 E2E tests (Login, Products, Cart…)
│   ├── test_login.py
│   ├── test_web.py
│   └── test_api.py
│
├── reports/                     # Generated Markdown reports
├── requirements.txt
└── requirements.flex.txt        # Flexible deps for CI/AI agent
```

---

## Getting Started

### Prerequisites
- Python 3.12+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/gilkalman-portfolio/automation.git
cd automation

# Install dependencies
pip install -r requirements.flex.txt

# Install Playwright browsers
python -m playwright install chromium
```

### Environment variables (local)

Create a `.env` file in the project root:

```bash
# .env — never commit this file
ANTHROPIC_API_KEY=sk-ant-...        # required only for --ai-fix
TELEGRAM_BOT_TOKEN=123456:ABC...    # required for Telegram notifications
TELEGRAM_CHAT_ID=-100123456789      # your chat or group ID
```

---

## Configuration

Edit `configuration/data.xml` to control runtime behaviour:

```xml
<config>
  <run>
    <env>stg</env>
    <headless>true</headless>
    <browsers>chromium</browsers>       <!-- chromium | firefox | webkit -->
    <retries>1</retries>
    <trace>retain-on-failure</trace>
    <screenshot>only-on-failure</screenshot>
  </run>
  <environments>
    <stg baseUrl="https://www.saucedemo.com/"/>
  </environments>
</config>
```

CLI overrides are also supported:

```bash
pytest --env=prod --browsers=firefox --headless=true
```

---

## Usage

### Run all tests
```bash
pytest
```

### Run by marker
```bash
pytest -m smoke
pytest -m regression
```

### Run with Allure report
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## Automated Test Runner

`automated_test_runner.py` runs a full cycle:

```
1. Run pytest → capture JSON + JUnit XML results
2. If failures + --ai-fix → Claude Agent analyses and fixes
3. Re-run only the failed tests to verify fixes
4. Generate Markdown report → reports/report_YYYYMMDD_HHMMSS.md
5. Send summary + report file to Telegram
```

### Commands

```bash
# Single run — always works, no API key needed
python automated_test_runner.py

# Smoke tests only
python automated_test_runner.py -m smoke

# With AI auto-fix (requires ANTHROPIC_API_KEY)
python automated_test_runner.py --ai-fix

# Scheduled loop every 24 hours (local)
python automated_test_runner.py --schedule

# Custom interval
python automated_test_runner.py --schedule --interval-hours 6
```

### Report example

```
# Automated Test Report — 20260407_020315

Status: ✅ ALL PASSING
Duration: 42.3s

| Metric   | Before | After |
|----------|--------|-------|
| ✅ Passed | 18     | 20    |
| ❌ Failed | 2      | 0     |
| 🔧 Fixed  | —      | 2     |
```

---

## CI/CD — GitHub Actions

The workflow `.github/workflows/scheduled_test_runner.yml` runs automatically:

| Trigger | When |
|---------|------|
| **Schedule** | Every day at 02:00 UTC |
| **Manual dispatch** | GitHub UI → Actions → Run workflow |

### Required secrets (GitHub → Settings → Secrets → Actions)

| Secret | Purpose |
|--------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Target chat / group ID |
| `ANTHROPIC_API_KEY` | Claude API key (only needed with `ai_fix=true`) |

### Manual dispatch options

- **marker** — filter tests: `smoke` / `regression` / `sanity` / blank (all)
- **ai_fix** — `true` to enable Claude AI fixing (requires `ANTHROPIC_API_KEY`)

---

## Contact

**Gil Kalman**  
Phone: 050-6323576  
GitHub: [github.com/gilkalman-portfolio/automation](https://github.com/gilkalman-portfolio/automation)

---

## License

This project is created for **portfolio and demonstration purposes**.
