#!/bin/bash

# Script to install Ollama and download the Gemma 3 model

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Check if installation was successful
if ! command -v ollama &> /dev/null; then
    echo "Ollama installation failed. Please install manually from https://ollama.com/"
    exit 1
fi

echo "Ollama installed successfully!"

# Start the Ollama service
echo "Starting Ollama service..."
ollama serve &

# Wait for the service to start
sleep 5

# Pull the Gemma 3 model
echo "Downloading Gemma 3 model (this may take some time)..."
ollama pull gemma3

echo "Setup complete! Ollama is running with Gemma 3 model available."
echo "The API is accessible at http://localhost:11434/api"