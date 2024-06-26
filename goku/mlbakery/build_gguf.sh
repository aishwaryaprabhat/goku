#!/bin/bash
repo=${1:-"microsoft/Phi-3-mini-4k-instruct-gguf"}
model=${2:-"Phi-3-mini-4k-instruct-q4.gguf"}
github_username=${3:-"aishwaryaprabhat"}
tag=ghcr.io/$github_username/mlbakery:$model

pip install huggingface-hub>=0.17.1 -q

echo "Downloading "$repo"/"$model 
huggingface-cli download $repo $model --local-dir . --local-dir-use-symlinks False

# Create a temporary directory for the Docker build context
temp_dir=$(mktemp -d "$(pwd)/tempdir.XXXXXXXX")
cp $model $temp_dir/

# Build the Docker image
docker build -f Dockerfile -t $tag $temp_dir

# Clean up the temporary directory
rm -rf $temp_dir