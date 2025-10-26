# ai/Dockerfile
# Start from an official, lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just the requirements file first to leverage caching
COPY requirements.txt .

# Upgrade pip first to resolve hash mismatch and dependency issues
RUN pip install --upgrade pip

# Install the dependencies (this may take a few minutes)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# The command to run when the container starts, on port 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]