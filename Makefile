IMAGE := ghcr.io/copelaje/stockapi:latest

.PHONY: build pull up down logs

build:
	docker build -t $(IMAGE) .

pull:
	docker compose pull

up: pull
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f
