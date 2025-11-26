Gil Kalman – QA Automation Portfolio
Python • Playwright • Pytest • AI Agent (MCP) • API & DB Testing • Scalable Test Frameworks
This repository showcases my professional QA automation work, including a modular Python-based Playwright + Pytest framework, advanced XML-driven configuration, workflows, Page Objects, dynamic test execution, and an integrated AI Automation Agent (MCP) capable of generating, analyzing, and modifying tests and code.

Designed as a real-world demonstration for interviews, engineering discussions, and hands-on evaluation.

Goals of this Project
Showcase clean, production-style automation code.
Demonstrate separation of concerns: configuration, fixtures, page objects, workflows, tests.
Provide dynamic framework behavior per project using a single codebase:
XML configuration (data.xml)
Environment variables
CLI overrides (Pytest options)
Demonstrate integration with AI Agent (MCP) for intelligent automation.
Tech Stack
Language: Python
Test Runner: Pytest
Browser Automation: Playwright
Test Design: Page Objects + Workflows
Config System: XML (data.xml) + config_loader.py
Reporting: Allure
AI Integration: MCP Agent (JetBrains / Playwright / Pytest)
IDE: JetBrains / PyCharm
Project Structure
.
├─ configuration/
│  └─ data.xml              # Main XML configuration
│
├─ utilities/
│  ├─ config_loader.py      # Loads & normalizes config
│  └─ manage_pages.py       # Central Page Objects manager
│
├─ page_objects/
│  └─ login_page.py         # Example POM
│
├─ workflows/
│  └─ web_workflow.py       # UI workflows (login, etc.)
│
├─ tests/
│  └─ test_login.py         # Example tests
│
├─ conftest.py              # All fixtures & integration logic
├─ requirements.txt
└─ README.md
Configuration (XML + loader)
The project supports dynamic configuration using:

configuration/data.xml
Environment variables (TEST_ENV, TEST_HEADLESS, etc.)
CLI parameters
This allows the framework to adjust to any project without touching the code.

Architecture Overview
1. Configuration Layer
Dynamic setup using XML, ENV overrides, and CLI.

2. Fixtures & Test Runner (Pytest + Playwright)
Manages browsers, contexts, traces, screenshots, filtering via tags.

3. Page Objects Layer
Clean separation of UI elements & low‑level actions.

4. Pages Manager
Centralized object creation, avoids duplication.

5. Workflows
High‑level business flows based on combined Page Objects.

6. Tests Layer
Simple, readable test files driven by workflows.

7. AI Agent (MCP) Layer
The framework works with an AI agent capable of:

Generating new tests automatically
Refactoring workflows & Page Objects
Finding missing coverage
Updating configuration
Running and evaluating results
Running the Project
Install dependencies
pip install -r requirements.txt
Install browsers
playwright install
Run tests
pytest
Override config
TEST_ENV=prod TEST_HEADLESS=false pytest
Roadmap
Already implemented
Playwright + Pytest framework
XML configuration system
Workflows layer
Allure integration
AI Agent (MCP) compatibility
Coming next
API testing module
DB testing module
Richer workflows
CI pipelines
Contact
Author: Gil Kalman Role: QA Engineer – Automation & Manual

This repository is part of my professional portfolio and is designed to demonstrate clean, scalable, real‑world automation practices.