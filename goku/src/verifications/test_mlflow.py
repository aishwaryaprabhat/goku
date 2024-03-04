import mlflow
from mlflow.tracking import MlflowClient
import pytest
import os
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import numpy as np
import time
import uuid
import tempfile
import shutil

# Setup necessary environment variables for MLflow
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000'
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# Ensure the MLFlow tracking URI is correctly set
mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])

# Required environment variables
REQUIRED_ENV_VARS = ['MLFLOW_TRACKING_URI', 'MLFLOW_S3_ENDPOINT_URL', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']

def check_env_vars():
    """
    Checks if all required environment variables are present.
    Raises an exception if any are missing.
    """
    missing_vars = [var for var in REQUIRED_ENV_VARS if os.environ.get(var) is None]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


# Check environment variables before proceeding
check_env_vars()

@pytest.fixture(scope="session")
def client():
    """Provides an MLflow Client for interacting with the MLflow server."""
    return MlflowClient()

@pytest.fixture(scope="session")
def test_experiment(client):
    """Creates a new experiment for the test session and provides its ID."""
    # Generate a unique experiment name using a timestamp or UUID
    experiment_name = f"test_experiment_{uuid.uuid4()}"
    experiment_id = client.create_experiment(experiment_name)
    yield experiment_id
    mlflow.delete_experiment(experiment_id)

# Example test that uses the new experiment
def test_experiment_tracking(client, test_experiment):
    run_name = "test_experiment_tracking_run"
    with mlflow.start_run(run_name=run_name, experiment_id=test_experiment):
        mlflow.log_param("param1", 5)
        mlflow.log_metric("metric1", 0.85)

    runs = client.search_runs(experiment_ids=[test_experiment], filter_string=f"tags.mlflow.runName = '{run_name}'")
    assert len(runs) == 1, "Run was not properly tracked."
    # Cleanup: Delete the run after verification
    for run in runs:
        client.delete_run(run.info.run_id)


def test_model_logging_and_registration(client, test_experiment):
    model_name = "TestLinearRegressionModel"
    with mlflow.start_run(experiment_id=test_experiment) as run:
        # Generate some dummy data
        X, y = make_regression(n_samples=100, n_features=2, noise=0.1)
        model = LinearRegression()
        model.fit(X, y)  # Train the model

        # Log the model
        mlflow.sklearn.log_model(model, "model")
        model_uri = f"runs:/{run.info.run_id}/model"
        result = mlflow.register_model(model_uri, model_name)
    
    model_version = result.version
    registered_model = client.get_model_version(model_name, model_version)
    assert registered_model.name == model_name, "Model was not registered correctly."
    # Cleanup
    client.delete_model_version(model_name, model_version)
    client.delete_registered_model(model_name)

def test_artifact_storage(client, test_experiment):
    # Create a temporary directory for the artifact
    temp_dir = tempfile.mkdtemp()
    artifact_path = os.path.join(temp_dir, "artifact.txt")
    with open(artifact_path, 'w') as f:
        f.write('This is a test artifact.')  # Create the artifact file

    with mlflow.start_run(experiment_id=test_experiment) as run:
        mlflow.log_artifact(artifact_path)
        run_id = run.info.run_id

    # Retrieve artifacts for the specific run
    artifacts = client.list_artifacts(run_id, path=None)
    expected_artifact_name = os.path.basename(artifact_path)
    artifact_paths = [artifact.path for artifact in artifacts]
    assert expected_artifact_name in artifact_paths, "Artifact was not stored correctly."

    client.delete_run(run_id)

    # Cleanup the temporary directory after the test
    shutil.rmtree(temp_dir)


# Test for Nested Runs (New in MLFlow 2.x)
def test_nested_runs(client):
    parent_run_name = "parent_run"
    child_run_name = "child_run"
    with mlflow.start_run(run_name=parent_run_name) as parent_run:
        with mlflow.start_run(run_name=child_run_name, nested=True) as child_run:
            mlflow.log_param("child_param", "nested")

    # Verify nested run
    child_runs = client.search_runs(experiment_ids=["0"], filter_string=f"tags.mlflow.parentRunId = '{parent_run.info.run_id}'")
    assert len(child_runs) == 1 and child_runs[0].data.params['child_param'] == "nested", "Nested run was not properly tracked."
    client.delete_run(child_run.info.run_id)
    client.delete_run(parent_run.info.run_id)


if __name__ == "__main__":
    pytest.main()