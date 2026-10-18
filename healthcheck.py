import json
import time
import requests


def check_service(name, url):
    start_time = time.perf_counter()

    try:
        response = requests.get(url, timeout=5)

        elapsed_time = time.perf_counter() - start_time
        response_time_ms = elapsed_time * 1000

        print(
            f"Service: {name} | "
            f"Status Code: {response.status_code} | "
            f"Response Time: {response_time_ms:.2f} ms"
        )

    except requests.exceptions.Timeout:
        elapsed_time = time.perf_counter() - start_time
        response_time_ms = elapsed_time * 1000

        print(
            f"Service: {name} | "
            f"Status: TIMEOUT | "
            f"Response Time: {response_time_ms:.2f} ms"
        )

    except requests.exceptions.RequestException as error:
        elapsed_time = time.perf_counter() - start_time
        response_time_ms = elapsed_time * 1000

        print(
            f"Service: {name} | "
            f"Status: ERROR | "
            f"Response Time: {response_time_ms:.2f} ms | "
            f"Details: {error}"
        )


def main():
    with open("services.json", "r", encoding="utf-8") as file:
        services = json.load(file)

    print("=== Service Health Check ===")

    for service in services:
        check_service(service["name"], service["url"])


if __name__ == "__main__":
    main()