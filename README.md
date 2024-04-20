# GOKU: <u>G</u>enAI<u>O</u>ps on <u>Ku</u>bernetes
[Work in Progress]
A reference architecture for performing Generative AI Operations (aka GenAIOps) using Kubernetes, with open source tools

![](docs/assets/screenshots/goku.webp)

## Table of Contents
- [Installation](#installation)
- [Features](#features)
  - [Model Ingestion](#model-ingestion)
  - [Distributed RAG Experimentation](#dream-distributed-rag-experimentation-framework)
  - [Model Serving](#model-serving)
  - [Vector Ingestion](#vector-ingestion)
  - [End-to-end RAG Evaluation](#end-to-end-rag-evaluation)
  - [Model Monitoring](#model-monitoring)
  
## Installation
For installation, follow the steps provided in [the setup doc](docs/installation_guide.md)

## Features
### Model Ingestion
![](docs/assets/architecture/model_ingestion.png)
GOKU uses a customizable Argo Workflows template to download models from Hugging Face and ingest them into MLFlow.
<details>
<summary>How to run</summary>
To run the model ingestion with the default image, follow these steps:

1. Navigate to the Argo Workflows UI (see steps in [the setup doc](docs/installation_guide.md) if unsure)
2. Enter the "goku" namespace and click on "SUBMIT NEW WORKFLOW"
3. Select "model-ingestion" as the template to be used
4. Enter the name of the model you want to ingest and click on "SUBMIT"
![](docs/assets/screenshots/mi_1.png)
5. You should see the model ingestion workflow running
![](docs/assets/screenshots/mi_2.png)
6. Once the workflow completes successfully, you should be able to see the model files saved as artifacts on mlflow
![](docs/assets/screenshots/mi_3.png)
7. You should also be able to verify that the model artifacts have been ingested successfully using MinIO console
![](docs/assets/screenshots/mi_4.png)
</details>

### DREAM: Distributed RAG Experimentation Framework
![](docs/assets/architecture/dream_archi.gif)
Distributed RAG Experimentation Framework (DREAM) presents a kubernetes native architecture and sample code to demonstrate how Retrieval Augmented Generation experiments, evaluation and tracking can be conducted in a distributed manner using Ray, LlamaIndex, Ragas, MLFlow and MinIO. 
Checkout the [DREAM README](./goku/dream/README.md) for details

### Model Serving
(WIP)
![](docs/assets/architecture/model_serving.png)

### Vector Ingestion
(WIP)
![](docs/assets/architecture/vector_ingestion.png)

### End-to-end RAG Evaluation
(WIP)
![](docs/assets/architecture/eval.png)

### Model Monitoring
(WIP)
![](docs/assets/architecture/monitoring.png)
