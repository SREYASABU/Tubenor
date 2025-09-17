FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .

COPY --from=ghcr.io/astral-sh/uv:0.8.17 /uv /uvx /bin/

RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY app /app/

CMD ["uv", "run", "fastapi", "run", "main.py", "--workers", "4"]
