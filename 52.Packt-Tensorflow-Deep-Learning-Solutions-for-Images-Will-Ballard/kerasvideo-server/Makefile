IMAGE ?= kerasvideo-server
CONTAINER ?= kerasvideo
PORT ?= 5000

install:
	pip install -r requirements.txt
.PHONY: install

#server will need to be running
test:
	curl -F file=@var/data/sample-0.png http://localhost:$(PORT)/mnist/classify
.PHONY: test

debug:
	python server.py
.PHONY: debug

samples:
	python dump_mnist.py
.PHONY: samples

var/data/mnist.keras:
	python train_mnist.py

## docker

docker-build:
	docker build -t $(IMAGE) .
.PHONY: docker-build

docker-run:
	docker run --rm -d --name $(CONTAINER) -p $(PORT):5000 $(IMAGE)
.PHONY: docker-run

#copy the sample digits baked into the image out to the host, for curl testing
docker-samples:
	mkdir -p var/data
	docker cp $(CONTAINER):/src/var/data/. var/data/
.PHONY: docker-samples

docker-logs:
	docker logs -f $(CONTAINER)
.PHONY: docker-logs

docker-stop:
	docker stop $(CONTAINER)
.PHONY: docker-stop
