# Automation Testing Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-Latest-orange.svg)](https://pytest.org/)

A **production-ready automation framework** showcasing clean, modular code with AI-powered testing capabilities and dynamic configuration management.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)

---

## Overview

This project demonstrates **professional-grade automation testing** with:

- **Clean, production-style code** with separation of concerns
- **Dynamic framework behavior** per project using a single codebase
- **XML-based configuration** for flexible test management
- **AI Agent (MCP)** integration for intelligent automation
- **Page Object Model** with centralized page management
- **Comprehensive reporting** with Allure

---

## Key Features

### Dynamic Configuration
- XML-based configuration (`data.xml`)
- Environment variables (TEST_ENV, TEST_HEADLESS, etc.)
- CLI parameters for runtime flexibility
- **No code changes needed** to adapt to different projects

### AI Integration
- **MCP Agent** support (JetBrains / Playwright / Pytest)
- Intelligent test automation capabilities
- Enhanced debugging and analysis

### Clean Architecture
- **Page Objects + Workflows** design pattern
- Centralized page management (`manage_pages.py`)
- Reusable fixtures and utilities
- Modular test structure

### Advanced Reporting
- **Allure** test reports with detailed insights
- Test execution analytics
- Failure screenshots and logs

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Test Runner** | Pytest |
| **Browser Automation** | Playwright |
| **Test Design** | Page Objects + Workflows |
| **Config System** | XML (data.xml) + config_loader.py |
| **Reporting** | Allure |
| **AI Integration** | MCP Agent (JetBrains / Playwright / Pytest) |
| **IDE** | JetBrains / PyCharm |

---

## Project Structure

```
automation/
├── configuration/
│   ├── data.xml                 # Main XML configuration
│   └── config_loader.py         # Loads & normalizes config
│
├── utilities/
│   └── manage_pages.py          # Central Page Objects manager
│
├── page_objects/
│   └── login_page.py            # Example Page Object Model
│
├── workflows/
│   └── web_workflow.py          # UI workflows (login, etc.)
│
├── tests/
│   ├── conftest.py              # All fixtures & integration logic
│   └── test_login.py            # Example tests
│
└── requirements.txt             # README.md Configuration (XML + loader)
```

---

## Architecture Overview

### 1. Configuration Layer
**Dynamic setup** using XML, ENV overrides, and CLI parameters.

```python
# configuration/data.xml
<Environment>
    <TEST_ENV>staging</TEST_ENV>
    <TEST_HEADLESS>false</TEST_HEADLESS>
</Environment>
```

This allows the framework to **adapt to any project** without touching the code.

---

### 2. Page Objects Layer
**Centralized management** of all page objects using `manage_pages.py`.

```python
# utilities/manage_pages.py
class PageManager:
    def __init__(self, page):
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        # Add more pages here
```

---

### 3. Workflows Layer
**Reusable business logic** separated from tests.

```python
# workflows/web_workflow.py
def login_workflow(page_manager, username, password):
    page_manager.login_page.navigate()
    page_manager.login_page.login(username, password)
```

---

### 4. Tests Layer
**Clean, readable tests** using fixtures and workflows.

```python
# tests/test_login.py
def test_successful_login(page_manager, config):
    login_workflow(
        page_manager,
        config['username'],
        config['password']
    )
    assert page_manager.dashboard_page.is_visible()
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/gilkalman-portfolio/automation.git
cd automation

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

---

## Configuration

### Environment Variables
Set these in your environment or `.env` file:

```bash
export TEST_ENV=staging          # Environment: staging, production
export TEST_HEADLESS=false       # Run with visible browser
export TEST_BROWSER=chromium     # Browser: chromium, firefox, webkit
```

### XML Configuration
Edit `configuration/data.xml`:

```xml
<Configuration>
    <Environment>
        <TEST_ENV>staging</TEST_ENV>
        <BASE_URL>https://staging.example.com</BASE_URL>
    </Environment>
    <Credentials>
        <username>test_user</username>
        <password>test_pass</password>
    </Credentials>
</Configuration>
```

### CLI Parameters
Override settings at runtime:

```bash
pytest --env=production --headless=true
```

---

## Usage

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_login.py
```

### Run with Specific Marker
```bash
pytest -m smoke
```

### Run with Allure Report
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Run in Headless Mode
```bash
pytest --headless=true
```

---

## Test Reports

Generate beautiful **Allure reports**:

```bash
# Generate report data
pytest --alluredir=allure-results

# View the report
allure serve allure-results
```

---

## Contributing

This is a **portfolio project** demonstrating professional automation skills. Feel free to explore the code structure and design patterns used.

---

## Contact

**Gil Kalman**  
Phone: 050-6323576  
GitHub: [github.com/gilkalman-portfolio/automation](https://github.com/gilkalman-portfolio/automation)

---

## License

This project is created for **portfolio and demonstration purposes**.

---

<div align="center">

**If you find this project helpful, please give it a star!**

</div>
