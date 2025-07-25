# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for ffmpeg, etc.)
RUN apt-get update && apt-get install -y ffmpeg build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env ./

# Copy the rest of the code
COPY . .


# Expose port
EXPOSE 8000

# Set environment variables (optional, but good practice)
ENV PORT 8000
ENV HOST 0.0.0.0

# Start FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

