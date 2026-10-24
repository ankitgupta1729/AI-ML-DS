## Setup

This project uses a local `uv` virtual environment in `.venv`.

To make the environment show up in Jupyter and VS Code kernel pickers, the
venv is registered as a global kernelspec:

```bash
uv sync
uvkernel -n cnn-tf-53 -d "53 CNN TF (.venv 3.13)" .
uvkernel --pin .
```

The notebook `1.ipynb` is pinned to the `cnn-tf-53` kernel so it opens with
the right interpreter automatically.
