shell:
	docker compose run --rm api python manage.py shell

migrations:
	docker compose run --rm api python manage.py makemigrations

migrate:
	docker compose run --rm api python manage.py migrate

superuser:
	docker compose run --rm api python manage.py createsuperuser

build:
	docker compose build

run:
	docker compose up

down:
	docker compose down
