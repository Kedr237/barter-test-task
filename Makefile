up:
	docker compose -f docker-compose.yml up -d --build --force-recreate --remove-orphans

stop:
	docker compose -f docker-compose.yml stop

down:
	docker compose -f docker-compose.yml down

logs:
	docker compose -f docker-compose.yml logs


# DOCKER_COMPOSE_FILE := docker-compose.yml
# ifeq ($(for), dev)
# 	DOCKER_COMPOSE_FILE := docker-compose.dev.yml
# endif

# up:
# 	docker compose -f $(DOCKER_COMPOSE_FILE) up -d --build --force-recreate --remove-orphans

# stop:
# 	docker compose -f $(DOCKER_COMPOSE_FILE) stop

# down:
# 	docker compose -f $(DOCKER_COMPOSE_FILE) down

# logs:
# 	docker compose -f $(DOCKER_COMPOSE_FILE) logs
