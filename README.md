# GOKU: <u>G</u>enAI<u>O</u>ps on <u>Ku</u>bernetes
A reference architecture for performing Generative AI Operations (aka GenAIOps) using Kubernetes, with open source tools

![](docs/assets/screenshots/goku.webp)


## Installation
For installation, follow the steps provided in [the setup doc](docs/installation_guide.md)

## Features
### Model Ingestion
![](docs/assets/architecture/model_ingestion.png)
GOKU uses a customisable Argo Workflows template to download models from Hugging Face and ingest them into MLFlow.
<details>
<summary>How to run</summary>
To run the model ingestion with the default image, follow the following steps:

1. Navigate to the Argo Workflows UI (see steps in [the setup doc](docs/installation_guide.md) if unsure)
2. Enter the "goku" namespace and click on "SUBMIT NEW WORKFLOW"
3. Select "model-ingestion" as the template to be used
4. Enter the name of the model you want to ingest and click on "SUBMIT"
![](docs/assets/screenshots/mi_1.png)
5. You should see the model ingestion workflow running
![](docs/assets/screenshots/mi_2.png)
6. Once the workflow completes successfully, you should be able to see the model files saved as artifacts on mlflow
![](docs/assets/screenshots/mi_3.png)
</details>
