# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Install netcat (nc) for waiting for the database or other services to be ready
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app code
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Expose the Django port
EXPOSE 8000

# Set the entrypoint script to run on container start
ENTRYPOINT ["/app/entrypoint.sh"]
