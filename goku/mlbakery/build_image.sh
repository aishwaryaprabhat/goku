#!/bin/bash

# Set default values for image name and tag
IMAGE_NAME=ghcr.io/aishwaryaprabhat/mlbakery
IMAGE_TAG=spacy_en_core

# Dockerfile contents
DOCKERFILE="
FROM ubuntu:latest

# Install necessary packages
RUN apt-get update && \
    apt-get install -y g++

RUN apt-get install -y python3 python3-pip git htop

# Copy the model file into the container
WORKDIR /models
COPY . .
"

# Function to print usage
print_usage() {
    echo "Usage: $0 [-n IMAGE_NAME] [-t IMAGE_TAG] MODEL1 MODEL2 ..."
    echo "  -n IMAGE_NAME   Set the name of the Docker image (default: $IMAGE_NAME)"
    echo "  -t IMAGE_TAG    Set the tag for the Docker image (default: $IMAGE_TAG)"
    echo "  MODEL1 MODEL2 ...  List of Hugging Face models to download"
}

# Parse command-line arguments
while getopts "n:t:h" opt; do
    case $opt in
        n)
            IMAGE_NAME=$OPTARG
            ;;
        t)
            IMAGE_TAG=$OPTARG
            ;;
        h)
            print_usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            print_usage
            exit 1
            ;;
    esac
done
shift $((OPTIND - 1))

# Check if at least one model is provided
if [ $# -eq 0 ]; then
    echo "Error: No models provided." >&2
    print_usage
    exit 1
fi

# Create a temporary directory
TEMP_DIR=$(mktemp -d)

# Write Dockerfile to temporary directory
echo "$DOCKERFILE" > "$TEMP_DIR/Dockerfile"

# Download models using Hugging Face CLI
echo "Downloading models..."
for MODEL in "$@"; do
    MODEL_DIR="$TEMP_DIR/$(basename "$MODEL")"
    mkdir -p "$MODEL_DIR"
    huggingface-cli download "$MODEL" --local-dir "$MODEL_DIR"
done

# Build Docker image
echo "Building Docker image $IMAGE_NAME:$IMAGE_TAG..."
docker build -t "$IMAGE_NAME:$IMAGE_TAG" "$TEMP_DIR"

# Clean up temporary directory
rm -rf "$TEMP_DIR"

echo "Docker image $IMAGE_NAME:$IMAGE_TAG built successfully."