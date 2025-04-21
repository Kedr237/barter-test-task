up:
	docker compose -f docker-compose.yml up -d --build --force-recreate --remove-orphans

watch:
	docker compose -f docker-compose.yml watch

stop:
	docker compose -f docker-compose.yml stop

down:
	docker compose -f docker-compose.yml down

logs:
	docker compose -f docker-compose.yml logs

clear:
	docker compose -f docker-compose.yml down -v --rmi all

up-test:
	docker compose -f docker-compose.test.yml up --build --force-recreate --remove-orphans --abort-on-container-exit

logs-test:
	docker compose -f docker-compose.test.yml logs

clear-test:
	docker compose -f docker-compose.test.yml down -v --rmi all