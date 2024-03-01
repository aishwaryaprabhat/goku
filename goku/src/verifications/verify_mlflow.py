import mlflow

# Set the MLflow tracking URI to your MLflow server's URL
mlflow.set_tracking_uri(os.getenv("MLFLOW_URI"))

def check_mlflow_status():
    try:
        # Attempt to list experiments as a way to check server status
        experiments = mlflow.list_experiments()
        if experiments:
            print("MLflow is up and running.")
        else:
            print("MLflow is up but no experiments were found.")
    except Exception as e:
        print(f"Failed to connect to MLflow server: {e}")

# Call the function to check MLflow status
check_mlflow_status()