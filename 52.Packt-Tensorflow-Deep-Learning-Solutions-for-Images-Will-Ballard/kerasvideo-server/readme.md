# Overview
This is a REST Server for Keras models, utilizing OpenAPI to serve image classification
models.

Input images are `POST` to the served APIs, and classification `JSON` results are returned.

# Quick Start
```
pip install -r requirements.txt
python train_mnist.py
python server.py
```

Open your browser to (http://localhost:5000/ui).


## Models
Models are pretrained and saved individually, and then served at REST API endpoints.

### `train_mnist.py`
Classification models are provided for MNIST digits, which creates a saved model file resulting
from Keras training. This trained models is then used as the classification function.

## `server.py`
The server is a python script
API endpoints handle posted files, and conversion to the appropriate vector encoding for use with
keras. Once a `POST` image is encoded, it is sent to the loaded model for classification. Once classified,
the classification results are serialized to JSON and returned.

## Utilities
`dump_mnist.py` is provided to create a set of image files from the encoded MNIST digit dataset in order to
exercise the post API. It writes `var/data/sample-0.png` ... `sample-9.png`, one correctly labelled example
per digit.

## Docker
The included Dockerfile will create a container, complete with the REST server -- and pretrained models. Distributing
your models to your running servers in practice is a mildly painful exercise, so packing the binary data of the
trained model into a Docker container eases deployment.

With this Docker based approach, the server and model are completely self contained.

The image is CPU-only (`python:3.11-slim`), so it builds and runs natively on Apple Silicon Macs -- there is
no GPU to pass through on a MacBook Air. Note that `tensorflow-cpu` publishes no aarch64 wheels; the plain
`tensorflow` package is used instead, which is CPU-only on arm64 anyway.

```
# build -- installs deps, trains the model, dumps sample digits (~10 min the first time)
docker build -t kerasvideo-server .

# run -- host port 5001, because macOS AirPlay Receiver (Control Center) already
# listens on 5000. The container itself always listens on 5000.
docker run --rm -d --name kerasvideo -p 5001:5000 kerasvideo-server

# pull the sample digits out of the image so you can post them
mkdir -p var/data && docker cp kerasvideo:/src/var/data/. var/data/

# predict
curl -F file=@var/data/sample-7.png http://localhost:5001/mnist/classify
# -> "{\"digit\": 7, \"confidence\": 0.99...}"

docker stop kerasvideo
```

Swagger UI is at (http://localhost:5001/ui).

Troubleshooting on macOS:

* `bind: address already in use` on 5000 -- that is AirPlay Receiver. Map a different host port
  (`-p 5001:5000`), or disable it under System Settings > General > AirDrop & Handoff.
* `error committing ...: input/output error` during build -- the host disk is full, so Docker's
  sparse VM disk image cannot grow. Free space, then `docker builder prune -af` and rebuild.

Build knobs:

* `--build-arg EPOCHS=1` -- train for fewer epochs while iterating (default 5).
* `-e PORT=8080` at run time -- change the in-container listen port.

Note on your own images: MNIST digits are white strokes on a black background. A photo or screenshot of a
digit is usually black-on-white and will classify poorly unless you invert it first.