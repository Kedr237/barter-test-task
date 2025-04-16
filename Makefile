up:
	docker compose -f docker-compose.yml up -d --build --force-recreate --remove-orphans $(for)

stop:
	docker compose -f docker-compose.yml stop $(for)

rm:
	docker compose -f docker-compose.yml down

logs:
	docker compose -f docker-compose.yml logs $(for)
