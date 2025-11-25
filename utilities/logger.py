import logging
import os
from pathlib import Path
from typing import Optional


_LOGGERS: dict[str, logging.Logger] = {}


def _logs_dir() -> Path:
    base = os.getenv("TEST_OUTPUT_DIR", ".")
    p = Path(base)
    logs = p / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    return logs


def get_logger(test_name: Optional[str] = None) -> logging.Logger:
    """

    logs/<test_name>.log
    """
    if not test_name:
        test_name = "session"

    if test_name in _LOGGERS:
        return _LOGGERS[test_name]

    logger = logging.getLogger(f"test.{test_name}")
    logger.setLevel(logging.INFO)
    logger.propagate = False  #

    logs_dir = _logs_dir()
    log_file = logs_dir / f"{test_name}.log"

    # formatter
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # local handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    _LOGGERS[test_name] = logger
    return logger
