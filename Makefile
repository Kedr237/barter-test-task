include .env

up:
ifeq ($(DEBUG), True)
	docker compose -f docker-compose.yml watch
else
	docker compose -f docker-compose.yml up -d --build --force-recreate --remove-orphans
endif

stop:
	docker compose -f docker-compose.yml stop

down:
	docker compose -f docker-compose.yml down

logs:
	docker compose -f docker-compose.yml logs

clear:
	docker compose -f docker-compose.yml down -v --rmi all
