all: build up create_user_db collectstatic create_cache_table migrate_db
all_no_cache: build_no_cache up collectstatic create_user_db create_cache_table migrate_db

init:
	pip install -r requirements.txt

create_user_db:
	docker exec --user postgres plan_heure_db /bin/sh -c "createuser plan_heure -s && createdb -U plan_heure plan_heure"

create_cache_table:
	docker exec plan_heure_web /bin/sh -c "python manage.py createcachetable" 

migrate_db:
	docker exec plan_heure_web /bin/sh -c 'python manage.py migrate'

import_data:
	docker exec plan_heure_web /bin/sh -c 'python manage.py import_data all'

cov_test:
	coverage run manage.py test

cov_report:
	coverage report

build:
	docker-compose build

build_no_cache:
	docker-compose build --no-cache

up:
	docker-compose up -d

up_no_d:
	docker-compose up

restart:
	docker-compose restart

collectstatic:
	docker exec plan_heure_web /bin/sh -c "python manage.py compilescss" && docker exec plan_heure_web /bin/sh -c "python manage.py collectstatic --noinput"

bash_nginx:
	docker exec -ti plan_heure_nginx bash

bash_web:
	docker exec -ti plan_heure_web bash

bash_db:
	docker exec -ti plan_heure_db bash

freeze:
	pip freeze > requirements.txt