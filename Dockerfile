# Use Python slim base image (small size)
FROM python:3.10-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install only necessary system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only source code (ignore heavy stuff via .dockerignore)
COPY . .

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Run Uvicorn server
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
