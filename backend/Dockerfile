# Start from an official, lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy just the requirements file first to leverage Docker's layer caching
COPY backend/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# The command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]