# service-healthcheck
A Python tool to monitor service availability and response times
# Service Health Check

A simple Python project that checks service availability and measures HTTP response times.

## Features

- Reads service URLs from a JSON configuration file.
- Sends HTTP GET requests.
- Measures response time in milliseconds.
- Displays HTTP status codes.
- Handles request timeouts and connection errors.

## Technologies Used

- Python
- Requests
- JSON
- Git and GitHub

## Project Structure

```text
service-healthcheck/
├── .gitignore
├── README.md
├── services.json
└── healthcheck.py
```

## Prerequisites

- Python 3
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/PremaNR72/service-healthcheck.git
cd service-healthcheck
```

Create and activate a virtual environment on Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependency:

```bash
python -m pip install requests
```

## Configuration

Edit `services.json` to add or remove services.

Example:

```json
[
    {
        "name": "Example Service",
        "url": "https://httpbin.org/status/200"
    }
]
```

## Usage

Run the health checker:

```bash
python healthcheck.py
```

The program displays each service's name, HTTP status code or error status, and response time in milliseconds.

## Future Improvements

- Classify services as UP or DOWN.
- Save results to a log file.
- Add response-time thresholds.
- Run checks periodically.
- Generate health-check reports.

## License

This project is intended for learning and educational purposes.