FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/production.txt

COPY backend/ ./backend/
COPY .env .env

WORKDIR /app/backend

EXPOSE 8000

CMD ["gunicorn", "motorbrain.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
