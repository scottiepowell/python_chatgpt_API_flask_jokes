#!/bin/sh

# Clone the repository
git clone https://github.com/scottiepowell/python_chatgpt_API_flask_jokes.git

# Change to the repository directory
cd python_chatgpt_API_flask_jokes

# Make sure you have a docker-compose.yaml file in the repository
if [ ! -f docker-compose.yaml ]; then
  echo "docker-compose.yaml file not found."
  exit 1
fi

# Build and run the services defined in the docker-compose.yaml file
docker-compose up -d

echo "Services started successfully."
