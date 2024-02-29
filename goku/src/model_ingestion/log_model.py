import os
import mlflow

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
MLFLOW_EXPERIMENT_NAME = os.getenv('MLFLOW_EXPERIMENT_NAME', 'mistralai')
MODEL_NAME = os.getenv('MODEL_NAME', 'Mixtral-8x7B-Instruct-v0.1')

def log_model(model_name):
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    with mlflow.start_run():
        mlflow.log_artifacts(model_name, artifact_path="model")
        print(f"Model {model_name} logged to MLflow.")

if __name__ == "__main__":
    log_model(MODEL_NAME)
