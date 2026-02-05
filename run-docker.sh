#!/bin/bash

# PsychoAI Bot - Docker runner
# Usage: ./run-docker.sh

set -e

IMAGE_NAME="psychoai-bot"
ENV_FILE=".env"

echo "🐳 PsychoAI Docker Runner"
echo "========================="

# Check .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Error: $ENV_FILE not found!"
    echo "   Copy .env.example to .env and fill in your keys."
    exit 1
fi

# Build image
echo "📦 Building Docker image..."
docker build -t $IMAGE_NAME .

# Run container
echo "🚀 Starting bot..."
echo "   Press Ctrl+C to stop"
echo ""

docker run -it --rm --env-file $ENV_FILE $IMAGE_NAME
