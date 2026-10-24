# CPU-only base image. Works natively on Apple Silicon (linux/arm64) as well as
# on linux/amd64 -- there is no CUDA/GPU on a MacBook Air, so the original
# nvidia/cuda base image is not usable here.
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # keep TensorFlow's C++ logging quiet (0=all ... 3=errors only)
    TF_CPP_MIN_LOG_LEVEL=2 \
    MODEL_PATH=/src/var/data/mnist.keras \
    PORT=5000

# unprivileged user to run the server
RUN useradd -m -s /bin/bash -u 1000 keras && \
    mkdir -p /src/var/data && \
    chown -R keras:keras /src

WORKDIR /src

# dependencies first, so code edits do not invalidate the (slow) pip layer
COPY requirements.txt /src/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /src/requirements.txt

# all the code
COPY --chown=keras:keras . /src

# train the model and dump a handful of sample PNGs to post at the API.
# ~2-4 minutes on Apple Silicon CPU; override with --build-arg EPOCHS=1 to iterate faster.
ARG EPOCHS=5
RUN EPOCHS=${EPOCHS} python train_mnist.py && \
    python dump_mnist.py && \
    chown -R keras:keras /src/var

USER keras
EXPOSE 5000
CMD ["python", "server.py"]
