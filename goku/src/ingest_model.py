import os
import argparse
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM
import mlflow

def ingest_model(model_name):
    
    # Downloading and saving the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.getenv('HUGGINGFACE_API_TOKEN'))
    model = AutoModelForCausalLM.from_pretrained(model_name, token=os.getenv('HUGGINGFACE_API_TOKEN'))

    
    temp_dir = "model_shards"
    experiment_name, run_name = model_name.split('/')[0], model_name.split('/')[1]
    # Create the directory if it doesn't exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the model to the new directory
    tokenizer.save_pretrained(temp_dir)
    model.save_pretrained(temp_dir)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run(run_name=run_name):
        mlflow.log_artifacts(temp_dir, temp_dir)
    

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download and save a model from Hugging Face.')

    parser.add_argument('--model', type=str, help='The model to be downloaded from Hugging Face')

    # Parse the command line arguments
    args = parser.parse_args()

    # Call download_model with CLI arguments or None (to use defaults)
    ingest_model(args.model)
