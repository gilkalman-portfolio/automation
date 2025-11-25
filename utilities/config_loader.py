from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional, Tuple

_CACHE: Optional[Dict[str, Any]] = None


def _module_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def _project_root() -> str:
    return os.path.dirname(_module_dir())


def _cfg_path(xml_path: Optional[str]) -> str:
    return xml_path or os.path.join(_project_root(), "configuration", "data.xml")


def _split_list(val: Optional[str]) -> List[str]:
    if not val:
        return []
    out: List[str] = []
    for part in val.split(","):
        p = part.strip().strip('"').strip("'")
        if p:
            out.append(p)
    return out


def _as_bool(val: Optional[str]) -> bool:
    return str(val).strip().lower() in {"1", "true", "yes", "on"}


def _norm_choice(val: Optional[str], default: str, allowed: Tuple[str, ...]) -> str:
    v = (val or default).strip().lower()
    if v not in allowed:
        raise ValueError(f"Invalid value '{val}'. Allowed: {allowed}")
    return v


def _read_credentials(root: ET.Element) -> Dict[str, Dict[str, str]]:
    creds: Dict[str, Dict[str, str]] = {}
    node = root.find("./credentials")
    if node is None:
        return creds
    for child in node:
        entry: Dict[str, str] = {}
        for k, v in child.attrib.items():
            entry[k] = v
        text = (child.text or "").strip()
        if text:
            entry["_text"] = text
        creds[child.tag] = entry
    return creds


def load_config(xml_path: Optional[str] = None, *, reload: bool = False) -> Dict[str, Any]:
    global _CACHE
    if _CACHE is not None and not reload:
        return _CACHE

    path = _cfg_path(xml_path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration XML not found at: {path}")

    tree = ET.parse(path)
    root = tree.getroot()

    run = root.find("./run") or ET.Element("run")
    env_name = (run.findtext("env") or "stg").strip()

    base_url_raw = (run.findtext("baseUrl") or "auto").strip()
    if base_url_raw.lower() == "auto":
        env_node = root.find(f'./environments/{env_name}')
        base_url = env_node.get("baseUrl") if env_node is not None else None
    else:
        base_url = base_url_raw

    headless = _as_bool(run.findtext("headless"))
    browsers = _split_list(run.findtext("browsers"))
    devices = _split_list(run.findtext("devices"))
    tags = _split_list(run.findtext("tags"))
    workers = int(run.findtext("workers") or 1)
    retries = int(run.findtext("retries") or 0)
    trace = (run.findtext("trace") or "off").strip()
    video = (run.findtext("video") or "off").strip()
    screenshot = (run.findtext("screenshot") or "only-on-failure").strip()

    env_override = os.getenv("TEST_ENV")
    if env_override:
        env_name = env_override.strip()

    base_url = os.getenv("TEST_BASE_URL", base_url)
    headless = _as_bool(os.getenv("TEST_HEADLESS", str(headless)))
    env_browsers = os.getenv("TEST_BROWSERS")
    env_devices = os.getenv("TEST_DEVICES")
    env_tags = os.getenv("TEST_TAGS")
    if env_browsers:
        browsers = _split_list(env_browsers)
    if env_devices:
        devices = _split_list(env_devices)
    if env_tags:
        tags = _split_list(env_tags)
    workers = int(os.getenv("TEST_WORKERS", workers))
    retries = int(os.getenv("TEST_RETRIES", retries))
    trace = os.getenv("TEST_TRACE", trace)
    video = os.getenv("TEST_VIDEO", video)
    screenshot = os.getenv("TEST_SCREENSHOT", screenshot)

    if not browsers:
        browsers = ["chromium"]
    browsers = [b.lower() for b in browsers]
    for b in browsers:
        if b not in {"chromium", "firefox", "webkit"}:
            raise ValueError(f"Unsupported browser '{b}'. Allowed: chromium, firefox, webkit")

    if not devices:
        devices = ["desktop"]
    devices = [d.strip() for d in devices if d.strip()]

    trace = _norm_choice(trace, "off", ("off", "on", "retain-on-failure"))
    video = _norm_choice(video, "off", ("off", "on", "retain-on-failure"))
    screenshot = _norm_choice(screenshot, "only-on-failure", ("off", "on", "only-on-failure"))

    if base_url_raw.lower() == "auto" and not base_url:
        raise ValueError(
            f"baseUrl=auto but environment '{env_name}' not found under <environments> in {path}"
        )

    credentials = _read_credentials(root)

    cfg: Dict[str, Any] = {
        "enabled": _as_bool(run.findtext("enabled")),
        "env": env_name,
        "base_url": base_url,
        "headless": bool(headless),
        "browsers": browsers,
        "devices": devices,
        "tags": tags,
        "workers": int(workers),
        "retries": int(retries),
        "trace": trace,
        "video": video,
        "screenshot": screenshot,
        "credentials": credentials,
        "_source": path,
    }

    _CACHE = cfg
    return cfg
