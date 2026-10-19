"""Core logic: check one service, with retries."""
import logging
import time
from dataclasses import dataclass
from typing import Optional

import requests

log = logging.getLogger("healthcheck")


@dataclass
class Result:
    name: str
    url: str
    ok: bool
    status: Optional[int]
    elapsed_ms: Optional[float]
    attempts: int
    error: Optional[str] = None


def _is_ok(status: int, expected: Optional[int]) -> bool:
    return status == expected if expected else status < 400


def check_service(service: dict, timeout: float = 5.0, retries: int = 2,
                  backoff: float = 1.0) -> Result:
    """Check one service. Retries on failure (so up to retries + 1 attempts)."""
    name, url = service["name"], service["url"]
    expected = service.get("expected_status")
    status = elapsed_ms = error = None
    ok = False
    attempts = 0

    for attempt in range(1, retries + 2):
        attempts = attempt
        start = time.perf_counter()
        try:
            resp = requests.get(url, timeout=timeout)
            elapsed_ms = (time.perf_counter() - start) * 1000
            status = resp.status_code
            ok = _is_ok(status, expected)
            error = None if ok else f"unexpected status {status}"
        except requests.RequestException as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000
            status, ok = None, False
            error = type(exc).__name__

        log.info("%s attempt %d/%d -> status=%s time=%.0fms ok=%s",
                 name, attempt, retries + 1, status, elapsed_ms, ok)
        if ok:
            break
        if attempt <= retries:
            time.sleep(backoff * attempt)

    if not ok:
        log.error("%s is DOWN (%s)", name, error)
    return Result(name, url, ok, status, elapsed_ms, attempts, error)
