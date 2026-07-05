IMAGE := stockapi:latest

.PHONY: build up down logs

build:
	docker build -t $(IMAGE) .

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f
