import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from healthcheck.checker import check_service
from healthcheck.cli import load_services, main
from healthcheck.report import render_table

SVC = {"name": "api", "url": "http://x.test"}


def fake(status):
    m = MagicMock()
    m.status_code = status
    return m


@patch("healthcheck.checker.requests.get")
def test_up_on_200(get):
    get.return_value = fake(200)
    r = check_service(SVC, retries=0)
    assert r.ok and r.status == 200 and r.attempts == 1


@patch("healthcheck.checker.requests.get")
def test_down_on_500(get):
    get.return_value = fake(500)
    r = check_service(SVC, retries=0)
    assert not r.ok and r.status == 500


@patch("healthcheck.checker.requests.get")
def test_retries_then_succeeds(get):
    get.side_effect = [fake(503), fake(503), fake(200)]
    r = check_service(SVC, retries=2, backoff=0)
    assert r.ok and r.attempts == 3


@patch("healthcheck.checker.requests.get")
def test_timeout_marks_down(get):
    get.side_effect = requests.Timeout()
    r = check_service(SVC, retries=1, backoff=0)
    assert not r.ok and r.error == "Timeout" and r.attempts == 2


@patch("healthcheck.checker.requests.get")
def test_expected_status_respected(get):
    get.return_value = fake(301)
    assert check_service({**SVC, "expected_status": 301}, retries=0).ok


def test_table_summary():
    from healthcheck.checker import Result
    out = render_table([Result("a", "u", True, 200, 12.0, 1),
                        Result("b", "u", False, None, None, 3, "Timeout")])
    assert "UP" in out and "DOWN" in out and "1/2 services up" in out


def test_bad_config_raises(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps([{"name": "no-url"}]))
    with pytest.raises(ValueError):
        load_services(str(p))


@patch("healthcheck.checker.requests.get")
def test_exit_codes(get, tmp_path):
    cfg = tmp_path / "s.json"
    cfg.write_text(json.dumps([SVC]))
    log = str(tmp_path / "l.log")
    args = ["-c", str(cfg), "-r", "0", "-l", log]
    get.return_value = fake(200)
    assert main(args) == 0
    get.return_value = fake(500)
    assert main(args) == 1
    assert main(["-c", "missing.json", "-l", log]) == 2
