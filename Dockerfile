# ---- Build stage ----
FROM python:3.11-slim AS base

# Set environment to avoid .pyc files and enable stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# ---- Runtime ----
EXPOSE 5000

# Use Gunicorn as the production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "run:app"]
