# tests/conftest.py — MCP-friendly
# - Supports TEST_OUTPUT_DIR (or --output-dir) for all artifacts
# - Exports Playwright trace on failure when trace=retain-on-failure
# - CLI overrides for env/base-url/browsers/devices/headless/etc.
# - Optional tag filtering via <tags> in data.xml
from __future__ import annotations

from utilities.logger import get_logger
import logging
import os
from pathlib import Path
from typing import Dict, Any, List
from uuid import uuid4

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from workflows.web_workflow import WebFlows
from utilities.config_loader import load_config

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig: pytest.Config,
                             test_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Override launch args for Playwright.
    Priority:
    1. --headed from CLI (highest)
    2. <headless> from data.xml
    3. fallback to default Playwright behavior
    """
    launch_options = {}

    # 1. CLI override: if user runs pytest --headed → always override
    if pytestconfig.getoption("--headed"):
        launch_options["headless"] = False

    # 2. XML override: only if CLI DIDN'T force headless/headed
    elif test_cfg.get("headless") is False:
        launch_options["headless"] = False
    else:
        launch_options["headless"] = True

    # Keep Playwright plugin options (channel, slowmo, etc)
    browser_channel_option = pytestconfig.getoption("--browser-channel")
    if browser_channel_option:
        launch_options["channel"] = browser_channel_option

    slowmo_option = pytestconfig.getoption("--slowmo")
    if slowmo_option:
        launch_options["slow_mo"] = slowmo_option

    return launch_options


# -----------------------------
# Output directory management
# -----------------------------
def _outdir() -> Path:
    base = os.getenv("TEST_OUTPUT_DIR", ".")
    p = Path(base)
    # create known subdirs
    for sub in ["reports", "screenshots", "traces", "videos", "allure-results", "logs"]:
        (p / sub).mkdir(parents=True, exist_ok=True)
    return p

# -----------------------------
# CLI flags (override XML/ENV)
# -----------------------------
def pytest_addoption(parser: pytest.Parser) -> None:
    try:
        parser.addoption("--env", action="store", default=None)
    except: pass
    try:
        parser.addoption("--browsers", action="store", default=None)
    except: pass
    try:
        parser.addoption("--devices", action="store", default=None)
    except: pass
    try:
        parser.addoption("--headless", action="store", default=None)
    except: pass
    try:
        parser.addoption("--workers", action="store", default=None)
    except: pass
    try:
        parser.addoption("--retries", action="store", default=None)
    except: pass
    try:
        parser.addoption("--output-dir", action="store", default=None)
    except: pass
    try:
        parser.addoption("--base-url", action="store", default=None)
    except:
        pass
    try:
        parser.addoption("--lo-trace", action="store", default=None,  choices=["off", "on", "retain-on-failure"], )
    except:
        pass
    try:
        parser.addoption("--lo-video", action="store", default=None, choices=["off", "on", "retain-on-failure"], )
    except:
        pass
    try:
        parser.addoption("--lo-screenshot", action="store", default=None, choices=["off", "on", "only-on-failure"],)
    except:
        pass


def _split_csv(val: str | None) -> List[str]:
    if not val:
        return []
    return [p.strip().strip('"').strip("'") for p in val.split(",") if p.strip()]

def _as_bool(val: str | None) -> bool | None:
    if val is None:
        return None
    return val.strip().lower() in {"1", "true", "yes", "on"}

def _apply_cli_overrides(cfg: Dict[str, Any], pytestconfig: pytest.Config) -> Dict[str, Any]:
    def opt(name: str) -> str | None:
        return pytestconfig.getoption(f"--{name}")

    if opt("env"):
        cfg["env"] = opt("env")
    if opt("base-url"):
        cfg["base_url"] = opt("base-url")
    if opt("browsers"):
        cfg["browsers"] = _split_csv(opt("browsers"))
    if opt("devices"):
        cfg["devices"] = _split_csv(opt("devices"))

    hb = _as_bool(opt("headless"))
    if hb is not None:
        cfg["headless"] = hb

    if opt("workers"):
        cfg["workers"] = int(opt("workers"))
    if opt("retries"):
        cfg["retries"] = int(opt("retries"))

    if opt("lo-trace"):
        cfg["trace"] = opt("lo-trace")
    if opt("lo-video"):
        cfg["video"] = opt("lo-video")
    if opt("lo-screenshot"):
        cfg["screenshot"] = opt("lo-screenshot")

    # manage TEST_OUTPUT_DIR via CLI
    if opt("output-dir"):
        os.environ["TEST_OUTPUT_DIR"] = opt("output-dir")  # visible to all code
        _outdir()  # ensure dirs

    return cfg



# -----------------------------
# Session configuration
# -----------------------------
@pytest.fixture(scope="session")
def test_cfg(pytestconfig: pytest.Config) -> Dict[str, Any]:
    cfg = load_config(reload=True)
    _apply_cli_overrides(cfg, pytestconfig)
    if not cfg.get("browsers"):
        cfg["browsers"] = ["chromium"]
    if not cfg.get("devices"):
        cfg["devices"] = ["desktop"]
    return cfg

def pytest_configure(config: pytest.Config) -> None:
    cfg = load_config(reload=True)
    cfg = _apply_cli_overrides(cfg, config)
    config._cached_cfg = cfg
    _outdir()  # ensure structure exists
    # "browsers taken according to the XML."
    if not getattr(config.option, "browser", None):
        config.option.browser = cfg.get("browsers", ["chromium"])
    config._metadata = {
        "env": cfg.get("env"),
        "browsers": ",".join(cfg.get("browsers", [])),
        "devices": ",".join(cfg.get("devices", [])),
        "headless": str(cfg.get("headless")),
        "trace": cfg.get("trace"),
        "video": cfg.get("video"),
        "screenshot": cfg.get("screenshot"),
    }


# -----------------------------
# Parametrization
# -----------------------------
def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    cfg = getattr(metafunc.config, "_cached_cfg", None) or load_config()
    # if "browser_name" in metafunc.fixturenames:
    #     metafunc.parametrize("browser_name", cfg.get("browsers", ["chromium"]), scope="session")
    if "device_name" in metafunc.fixturenames:
        metafunc.parametrize("device_name", cfg.get("devices", ["desktop"]), scope="session")

# -----------------------------
# Core fixtures
# -----------------------------
@pytest.fixture(scope="session")
def base_url(test_cfg: Dict[str, Any]) -> str:
    return test_cfg.get("base_url") or "about:blank"

# @pytest.fixture(scope="session")
# def headless(test_cfg: Dict[str, Any]) -> bool:
#     return bool(test_cfg.get("headless", True))

@pytest.fixture(scope="session")
def trace_mode(test_cfg: Dict[str, Any]) -> str:
    return test_cfg.get("trace", "off")

@pytest.fixture(scope="session")
def video_mode(test_cfg: Dict[str, Any]) -> str:
    return test_cfg.get("video", "off")

@pytest.fixture(scope="session")
def screenshot_mode(test_cfg: Dict[str, Any]) -> str:
    return test_cfg.get("screenshot", "only-on-failure")

@pytest.fixture(scope="session")
def context_kwargs(device_name: str) -> Dict[str, Any]:
    if device_name.lower() == "desktop":
        return {}
    # For Playwright v1.46+, devices are predefined - using a simple approach
    # If you need specific device presets, define them here
    devices_dict = {
        "iPhone 12": {"viewport": {"width": 390, "height": 844}, "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"},
        "Pixel 5": {"viewport": {"width": 393, "height": 851}, "user_agent": "Mozilla/5.0 (Linux; Android 12)"},
    }
    preset = devices_dict.get(device_name)
    if not preset:
        raise RuntimeError(f"Unknown device: {device_name}")
    return preset

@pytest.fixture(scope="function")
def context(browser: Browser, context_kwargs: Dict[str, Any], trace_mode: str, video_mode: str) -> BrowserContext:
    kwargs = dict(context_kwargs)
    out = _outdir()
    if video_mode != "off":
        kwargs["record_video_dir"] = str(out / "videos")
    ctx = browser.new_context(**kwargs)
    if trace_mode in {"on", "retain-on-failure"}:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield ctx
    if trace_mode in {"on", "retain-on-failure"}:
        try:
            ctx.tracing.stop()
        except Exception:
            pass
    ctx.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, base_url: str) -> Page:
    pg = context.new_page()
    if base_url and base_url != "about:blank":
        pg.goto(base_url)
    return pg

@pytest.fixture
def web_workflow(page):
    return WebFlows(page)

@pytest.fixture(scope="function")
def logger(request) -> logging.Logger:
    """
    "Returns a per-test logger that writes to a file in the logs directory."
    """
    test_name = request.node.name
    return get_logger(test_name)

@pytest.fixture(scope="function", autouse=True)
def capture_console_logs(page: Page, logger: logging.Logger):
    """
    Captures browser console logs (console.log / error / warn / info)
    and writes them into the per-test logger.
    """
    def _log_console(msg):
        try:
            logger.info(f"[CONSOLE] {msg.type()} - {msg.text()}")
        except Exception:
            # Don't fail a test due to a logging issue
            pass

    page.on("console", _log_console)
    yield
    # No special teardown is needed – the page is closed by the existing fixture.

# -----------------------------
# Failure hooks
# -----------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        setattr(item, "_test_failed", rep.failed)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_teardown(item: pytest.Item, nextitem):
    outcome = yield
    cfg = getattr(item.config, "_cached_cfg", None) or load_config()
    screenshot_mode = cfg.get("screenshot", "only-on-failure")
    trace_mode = cfg.get("trace", "off")
    failed = bool(getattr(item, "_test_failed", False))

    out = _outdir()
    safe = item.name.replace("/", "_").replace("\\", "_").replace(":", "_")

    # Screenshots
    page: Page | None = item.funcargs.get("page") if hasattr(item, "funcargs") else None
    if page and (screenshot_mode == "on" or (screenshot_mode == "only-on-failure" and failed)):
        page.screenshot(path=str(out / "screenshots" / f"{safe}.png"))

    # Trace export only on failure and only if policy is retain-on-failure
    if trace_mode == "retain-on-failure" and failed:
        ctx = item.funcargs.get("context")
        if ctx:
            try:
                ctx.tracing.stop(path=str(out / "traces" / f"{safe}_{uuid4().hex}.zip"))
            except Exception:
                pass

# -----------------------------
# Optional: filter by tags from data.xml
# -----------------------------
def pytest_collection_modifyitems(config, items):
    cfg = getattr(config, "_cached_cfg", None) or load_config()
    tags = cfg.get("tags", [])
    if not tags:
        return
    selected = []
    for it in items:
        markers = {m.name for m in it.iter_markers()}
        if markers & set(tags):
            selected.append(it)
    if selected:
        items[:] = selected
