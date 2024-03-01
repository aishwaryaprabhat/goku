import os
import argparse
from transformers import AutoModel, AutoTokenizer

def download_model(model_name="Mistral-7B-Instruct-v0.2"):
    # Use environment variables as defaults if no arguments are provided

    if model_name is None:
        model_name = os.getenv("HF_MODEL_NAME", model_name)

    # Downloading and saving the model and tokenizer
    model = AutoModel.from_pretrained(repo)
    tokenizer = AutoTokenizer.from_pretrained(repo)

    model.save_pretrained(f"./{model_name}")
    tokenizer.save_pretrained(f"./{model_name}")
    print(f"Model and tokenizer saved to ./{model_name}")
    

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download and save a model from Hugging Face.')

    parser.add_argument('--model', type=str, help='The name under which to save the model and tokenizer.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Call download_model with CLI arguments or None (to use defaults)
    download_model(args.model)
