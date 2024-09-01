.PHONY: env
env:
	cp .env.example .env

.PHONY: build
build:
	docker compose build

build--no-cache:
	docker compose build --no-cache

.PHONY: up
up:
	docker compose up

.PHONY: up-d
up-d:
	docker compose up -d

.PHONY: dev
dev:
	@make build
	@make up-d

.PHONY: logs
logs:
	docker compose logs -f

.PHONY: stop
stop:
	docker compose stop

.PHONY: kill
kill:
	docker compose kill

.PHONY: down
down:
	docker compose down

.PHONY: prune
prune:
	docker image prune

.PHONY: clean
clean:
	docker rm -f `docker ps -aq`
	docker system prune -af

.PHONY: remove-none
remove-none:
	docker images | awk '/none/{print $3}' | xargs docker rmi

.PHONY: exec
exec:
	docker compose exec api bash

.PHONY: test
test:
	docker compose exec api pytest --cov=./ --cov-report term-missing:skip-covered

.PHONY: black
black:
	docker compose exec api black .

.PHONY: isort
isort:
	docker compose exec api isort .

.PHONY: flake8
flake8:
	docker compose exec api flake8 .

.PHONY: lint
lint:
	@make black
	@make isort
	@make flake8
