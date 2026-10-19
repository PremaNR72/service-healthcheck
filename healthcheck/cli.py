"""Command-line entry point."""
import argparse
import json
import logging
import sys

from .checker import check_service
from .report import render_table


def load_services(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    services = data.get("services", data) if isinstance(data, dict) else data
    for s in services:
        if "name" not in s or "url" not in s:
            raise ValueError(f"each service needs 'name' and 'url': {s}")
    return services


def parse_args(argv=None):
    p = argparse.ArgumentParser(prog="healthcheck",
                                description="Check service health after a deployment.")
    p.add_argument("-c", "--config", default="services.json", help="path to services JSON")
    p.add_argument("-t", "--timeout", type=float, default=5.0, help="request timeout (s)")
    p.add_argument("-r", "--retries", type=int, default=2, help="retries per failed check")
    p.add_argument("--backoff", type=float, default=1.0, help="base wait between retries (s)")
    p.add_argument("-l", "--log-file", default="healthcheck.log", help="log file path")
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    logging.basicConfig(filename=args.log_file, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        services = load_services(args.config)
    except (OSError, ValueError) as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 2

    results = [check_service(s, args.timeout, args.retries, args.backoff)
               for s in services]
    print(render_table(results))
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
