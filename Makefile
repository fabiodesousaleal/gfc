.PHONY: build run start stop restart remove help logs migrate createuser
IMAGE_NAME = fabiodesousaleal/gfc:v1.6
CONTAINER_NAME = ficha_app
HOST_PATH = $(shell pwd)

help:
	@echo "Usage:"
	@echo "  make up       	  Faz o build e controi a Imagem"
	@echo "  make build       Constrói a imagem Docker"
	@echo "  make run         Inicializa um contêiner"
	@echo "  make start       Inicia um contêiner parado"
	@echo "  make stop        Para o contêiner"
	@echo "  make restart     Reinicia o contêiner (equivalente a stop e start)"
	@echo "  make remove      Remove o contêiner"
	@echo "  make help        Exibe as opções disponíveis de ajuda"
	@echo "  make logs        Visualiza os logs da aplicação"
	@echo "  make migrate     Visualiza os logs da aplicação"
	@echo "  make createuser  Cria um usuário"


build:
	docker build -t $(IMAGE_NAME) .

run: 
	docker run -d --name $(CONTAINER_NAME) -p 5000:5000 -v $(shell realpath $(HOST_PATH)):/app $(IMAGE_NAME)

start:
	docker start $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)

restart: stop start

remove:
	docker rm $(CONTAINER_NAME) --force

logs:
	docker logs -f $(CONTAINER_NAME)

migrate:
	python3.11 migrations/1_inicial.py && echo "Migrações realizadas com sucesso!"

up: build run migrate

createuser:force
	docker exec -it $(CONTAINER_NAME) bash -c 'read -p "Digite o nome de usuário:" usuario; read -p "Digite a senha: " senha; python -c "from app import createuser; createuser(\"$${usuario}\", \"$${senha}\")"'

force: