# Use stable slim base
FROM python:3.11-slim

# Prevent bytecode + enable live logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install ONLY essential system packages (remove build-essential if not compiling)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy only app code (after installing deps)
COPY . .

# Run app (Render/Railway set PORT env var)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
