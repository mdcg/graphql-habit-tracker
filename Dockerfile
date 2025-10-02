ARG PYTHON_VERSION=3.11-alpine
FROM python:${PYTHON_VERSION} AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    bash \
    curl \
    make

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser -D appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

ENV MONGO_URI="mongodb://mongo:27017/appdb" \
    APP_HOST="0.0.0.0" \
    APP_PORT="8000"

ENTRYPOINT ["python", "-m", "application.api"]
