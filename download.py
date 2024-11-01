import pathlib

from huggingface_hub import snapshot_download

model_dir = pathlib.Path("/root/autodl-tmp/kzou/LLM-based-AI-Assistant/models/llm/")
snapshot_download("Jamacio/ggml-model-q4_0", repo_type="model", local_dir=model_dir)