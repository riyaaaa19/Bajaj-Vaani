FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for your libs
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libgl1 \
    curl \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

EXPOSE 8000

CMD CMD ["/bin/bash", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]


