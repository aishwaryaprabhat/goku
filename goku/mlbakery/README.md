# MLBakery
![MLBakery](assets/mlbakery.webp)
MLBakery is a subproject under [goku](../../README.md) that is aimed at creating lightweight base images with AI/ML artefacts, especially small language models and embedding models, for easier portability. Some of the pre-built images are released as packages that can be found in the parent project's ghcr. Ideally, though, you will use the scripts to build your own images :)

## Example Usage
```
bash build_gguf.sh microsoft/Phi-3-mini-4k-instruct-gguf Phi-3-mini-4k-instruct-fp16.gguf
```

## Available Images

| Image                                | Model Source             | Image Size |
|---------------------------------------|--------------------------|------------|
| [mlbakery:Phi-3-mini-4k-instruct-q4.gguf](https://github.com/aishwaryaprabhat/goku/pkgs/container/mlbakery/215241701?tag=Phi-3-mini-4k-instruct-q4.gguf)   | [Source](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/tree/main)              | 2.83GB     |
| [mlbakery:Phi-3-mini-4k-instruct-fp16.gguf](https://github.com/aishwaryaprabhat/goku/pkgs/container/mlbakery/215238297?tag=Phi-3-mini-4k-instruct-fp16.gguf)   | [Source](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/tree/main)              | 8.08GB   |
| [mlbakery:gemma-2b-it-q4_k_m.gguf](https://github.com/aishwaryaprabhat/goku/pkgs/container/mlbakery/215226227?tag=gemma-2b-it-q4_k_m.gguf)     | [Source](https://huggingface.co/lmstudio-ai/gemma-2b-it-GGUF/tree/main)         | 1.93GB     |
| [mlbakery:gemma-2b-it-q8_0gguf](https://github.com/aishwaryaprabhat/goku/pkgs/container/mlbakery/215224594?tag=gemma-2b-it-q8_0.gguf)     | [Source](https://huggingface.co/lmstudio-ai/gemma-2b-it-GGUF/tree/main)         | 3.1GB     |
