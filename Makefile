.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

MYSQL_DOCKER_RUN := docker-compose exec mysql
REDIS_DOCKER_RUN := docker-compose exec redis
DJANGO_DOCKER_RUN := docker-compose exec web
TMUXP := /home/qiaocc/.venv/test_env/bin/tmuxp

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

sep--sep-a: ## ========== 开发时命令 ==============

all-build-up: ## build and compose up
	docker-compose up --build

all-up: ## compose up
	docker-compose up

all-down: ## build and compose up
	docker-compose down

django-before-up: ## some deamons
	docker-compose up -d redis mysql

django-runserver: ## runserver
	docker-compose up web

django-manager: ## Enter python manage.py
	$(DJANGO_DOCKER_RUN) python manage.py

django-console: ## Enter Django Console
	$(DJANGO_DOCKER_RUN) python manage.py shell

shell: ## Enter Shell
	$(DJANGO_DOCKER_RUN) bash

dbshell: ## Enter mysql
	$(MYSQL_DOCKER_RUN) sh -c 'exec mysql -ujason -p123'

redis-shell: ## Enter mysql
	$(REDIS_DOCKER_RUN) sh -c 'redis-cli -a 123'

django-celeryworker: ## celeryworker
	 docker-compose up celeryworker

django-celeryflower: ## celeryflower
	docker-compose up celeryflower

django-celerybeat: ## celerybeat
	docker-compose up celerybeat

tmuxp: ## start tmuxp
	$(TMUXP) load tmuxp.yml


sep--sep-b: ## ========== 测试与代码质量 ==============

lint: ## check style with flake8
	@echo "--> Linting python"
	black .
	@echo ""

sort: # sort import with isort
	@echo "--> Sort python imort"
	isort -rc .
	@echo ""


sep--sep-c: ## ========== 文件清理相关 ==============

clean: clean-build clean-pyc ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@echo "--> Cleaning build artifacts"
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	@echo ""

clean-pyc: ## remove Python file artifacts
	@echo "--> Cleaning pyc"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


sep--sep-d: ## ========== 部署命令 ==============
deploy:	## deploy project
	@echo "--> Deploy project"
	fab -H tx -S ~/.ssh/config deploy