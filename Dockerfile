FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
# We need build-essential and wget for TA-Lib if we build from source, 
# but let's try to keep it slim. valid ta-lib-bin usually works for linux.
# We also might need git for some packages.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY trading_system/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Command to run the application (will be overridden by docker-compose or specific command)
CMD ["python", "main.py"]
