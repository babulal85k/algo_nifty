"""
FULL LINE-BY-LINE DIAGNOSTICS
Non-intrusive tracing for algo execution
"""

import json
import datetime
import traceback
import os

DIAG_FILE = "diagnostics.log"
JSON_FILE = "diagnostics.jsonl"  # one JSON per line


def _ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(step, message, data=None, level="INFO"):
    """
    Human + machine readable logging
    """
    record = {
        "time": _ts(),
        "level": level,
        "step": step,
        "message": message,
        "data": data,
    }

    # ---- text log (readable) ----
    with open(DIAG_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{record['time']}] [{level}] [{step}] {message}\n"
        )
        if data is not None:
            f.write(f"    DATA: {data}\n")

    # ---- structured log (JSON) ----
    with open(JSON_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def trace(step):
    """
    Decorator for function-level tracing
    """
    def decorator(fn):
        def wrapper(*args, **kwargs):
            log(step, f"ENTER {fn.__name__}", {
                "args": str(args),
                "kwargs": kwargs
            })
            try:
                result = fn(*args, **kwargs)
                log(step, f"EXIT {fn.__name__}", {"result": str(result)})
                return result
            except Exception as e:
                log(
                    step,
                    f"EXCEPTION in {fn.__name__}",
                    {"error": str(e), "trace": traceback.format_exc()},
                    level="ERROR",
                )
                raise
        return wrapper
    return decorator


def checkpoint(step, condition, message, data=None):
    """
    Explicit branch decision logging
    """
    if condition:
        log(step, f"✔ PASS: {message}", data)
    else:
        log(step, f"✖ FAIL: {message}", data, level="WARN")
    return condition