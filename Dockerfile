# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory content into the container
COPY . .

COPY ./app /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make the start.sh script executable
RUN chmod +x /app/start.sh

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the start.sh script
CMD ["./start.sh"]
