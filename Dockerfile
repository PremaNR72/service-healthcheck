FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY healthcheck/ healthcheck/
COPY services.json .
ENTRYPOINT ["python", "-m", "healthcheck"]
CMD ["--config", "services.json"]
