import os
import mlflow
from mlflow.tracking import MlflowClient

# Configure MLflow
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
if not MLFLOW_TRACKING_URI:
    raise ValueError("MLFLOW_TRACKING_URI environment variable is not set.")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

EXPERIMENT_NAME = "MLFlowVerification"

def create_artifact(content="This is a test artifact."):
    """Create a temporary text file as an artifact."""
    artifact_path = "test_artifact.txt"
    with open(artifact_path, "w") as f:
        f.write(content)
    return artifact_path

def log_and_cleanup_artifact():
    client = MlflowClient()

    # Ensure the experiment exists and get its ID
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    if experiment:
        experiment_id = experiment.experiment_id
    else:
        experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    
    # Start a new MLflow run
    with mlflow.start_run(experiment_id=experiment_id) as run:
        # Create an artifact
        artifact_path = create_artifact()
        
        # Log the artifact
        mlflow.log_artifact(artifact_path)
        print("Artifact logged successfully.")
        
        # Clean up local artifact file
        os.remove(artifact_path)
    
    # Delete the run for cleanup
    client.delete_run(run.info.run_id)
    print(f"Run {run.info.run_id} and its artifacts deleted successfully.")

if __name__ == "__main__":
    log_and_cleanup_artifact()
