import os
import argparse
from transformers import AutoModel, AutoTokenizer

def download_model(repo=None, model_name=None):
    # Use environment variables as defaults if no arguments are provided
    if repo is None:
        repo = os.getenv("HUGGINGFACE_REPO", "mistralai/Mixtral-8x7B-Instruct-v0.1")
    if model_name is None:
        model_name = os.getenv("MODEL_NAME", "Mixtral-8x7B-Instruct-v0.1")

    # Downloading and saving the model and tokenizer
    model = AutoModel.from_pretrained(repo)
    tokenizer = AutoTokenizer.from_pretrained(repo)

    model.save_pretrained(f"./{model_name}")
    tokenizer.save_pretrained(f"./{model_name}")
    print(f"Model and tokenizer saved to ./{model_name}")
    

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download and save a model from Hugging Face.')

    # Adding optional arguments
    parser.add_argument('--repo', type=str, help='The Hugging Face repository to download the model from.')
    parser.add_argument('--model', type=str, help='The name under which to save the model and tokenizer.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Call download_model with CLI arguments or None (to use defaults)
    download_model(args.repo, args.model)
