# Base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements.txt to container and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the Flask app to container
COPY . .

# Expose port 5000
EXPOSE 5000

# Start Flask app
CMD ["python3", "app.py"]