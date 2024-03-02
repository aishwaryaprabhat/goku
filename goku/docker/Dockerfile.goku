FROM ghcr.io/mlflow/mlflow:v2.10.2
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ingest_model.py .
