# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Install system dependencies (pg_isready + netcat)
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x ./entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
