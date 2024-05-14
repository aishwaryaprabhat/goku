#!/bin/bash
repo=${1:-"sentence-transformers/all-mpnet-base-v2"}
model_name=${2:-"all-mpnet-base-v2"}
github_username=${3:-"aishwaryaprabhat"}
tag=ghcr.io/$github_username/mlbakery:$model_name

pip install sentence-transformers>=2.2.2

echo "Downloading $repo"

# Create a temporary directory for the model download
temp_dir=$(mktemp -d "$(pwd)/tempdir.XXXXXXXX")
python - << EOF
from sentence_transformers import SentenceTransformer

model_name = "$repo"
save_path = "$temp_dir/$model_name"
model = SentenceTransformer(model_name)
model.save(save_path)
print(f"Model downloaded and saved to {save_path}")
EOF

# Build the Docker image
docker build -f Dockerfile -t $tag $temp_dir

# Clean up the temporary directory
rm -rf $temp_dir