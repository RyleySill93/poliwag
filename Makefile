# Database functions
setup-db:
	./backend/scripts/setup_db.sh

migrate:
	python backend/manage.py migrate

migrations:
	python backend/manage.py makemigrations

reset-db:
	python backend/manage.py reset_db --noinput
	echo "database has been reset"

backup-db:
	python backend/manage.py upload_demo_data

restore-db:
	python backend/manage.py load_demo_data


shell:
	python backend/manage.py shell_plus

dbshell:
	python backend/manage.py dbshell

# App functions
dev-frontend:
	ESLINT_NO_DEV_ERRORS=true TSC_COMPILE_ON_ERROR=true yarn start

dev-backend:
	python backend/manage.py runserver

dev-celery:
	cd backend && celery -A poliwag.celery worker -E -Q user_waiting -l DEBUG -Ofair --concurrency=2 --max-tasks-per-child=10

dev-celery-beat:
	cd backend && celery -A poliwag.celery beat -l DEBUG --max-interval 10

# Test functions
test-unit:
	pytest backend/tests/unit

test-api:
	pytest backend/tests/api

test-api-fast:
	pytest backend/tests/api --reuse-db

test-backend:
	pytest backend/tests/backend

test-backend-fast:
	pytest backend/tests/backend --reuse-db

# Utility functions
deploy-backend:
	python -m infra.tools.ops deploy backend

deploy-backend-full:
	python -m infra.tools.ops deploy backend_full

deploy-frontend:
	python -m infra.tools.ops deploy frontend

deploy-landing-page:
	python landing-page/deploy.py
	echo "landing page has been deployed"

ssh:
	python -m infra.tools.ops utils ssh
