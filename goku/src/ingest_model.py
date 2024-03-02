import os
import argparse
from transformers import AutoModel, AutoTokenizer

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
MLFLOW_EXPERIMENT_NAME = os.getenv('MLFLOW_EXPERIMENT_NAME', 'mistralai')
HF_MODEL_NAME = os.getenv('HF_MODEL_NAME', 'mistralai/Mistral-7B-Instruct-v0.2')

def ingest_model(model_name="mistralai/Mistral-7B-Instruct-v0.2"):
    # Use environment variables as defaults if no arguments are provided

    model_name = "mistralai/Mistral-7B-Instruct-v0.2"

    # Downloading and saving the model and tokenizer
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    with mlflow.start_run():
        mlflow.log_artifacts(model)
        print(f"Model {model_name} logged to MLflow.")

        mlflow.log_artifacts(tokenizer)
        print(f"Tokenizer {tokenizer} logged to MLflow.")
    

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download and save a model from Hugging Face.')

    parser.add_argument('--model', type=str, help='The name under which to save the model and tokenizer.')

    # Parse the command line arguments
    args = parser.parse_args()

    # Call download_model with CLI arguments or None (to use defaults)
    ingest_model(args.model)
