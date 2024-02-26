import os
from transformers import AutoModel, AutoTokenizer

REPO = os.getenv("HUGGINGFACE_REPO", "mistralai/Mixtral-8x7B-Instruct-v0.1")
MODEL = os.getenv("MODEL_NAME", "Mixtral-8x7B-Instruct-v0.1")

model = AutoModel.from_pretrained(REPO)
tokenizer = AutoTokenizer.from_pretrained(REPO)

model.save_pretrained(f"./{MODEL}")
tokenizer.save_pretrained(f"./{MODEL}")
print(f"Model and tokenizer saved to ./{MODEL}")
