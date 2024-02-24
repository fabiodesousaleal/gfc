.PHONY: build start stop restart help

IMAGE_NAME = fabiodesousaleal/gfc:v1.2.0
CONTAINER_NAME = gfc_app
HOST_PATH = $(shell pwd)  # Obtém o caminho absoluto do diretório atual

help:
	@echo "Usage:"
	@echo "  make build       Build the Docker image"
	@echo "  make start       Build and start the Docker container"
	@echo "  make stop        Stop the Docker container"
	@echo "  make restart     Stop and restart the Docker container"
	@echo "  make help        Show this help message"

build:
	docker build -t $(IMAGE_NAME) .

start: build
	docker run -d --name $(CONTAINER_NAME) -p 5000:5000 -v $(HOST_PATH):/app $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

restart: stop start
