DJANGO_DOCKER_RUN := docker exec -i -t django-blog_django_1
MYSQL_DOCKER_RUN := docker exec -i -t django-blog_mysql_1


sep--sep-a: ## ========== 开发时命令 ==============

django-build-up: ## build and compose up
	docker-compose -f develop.yml up --build

django-down: ## build and compose up
	docker-compose -f develop.yml down

django-before-up: ## some deamons
	docker-compose -f develop.yml up -d redis mysql rabbitmq celeryflower

django-runserver: ## runserver
	docker-compose -f develop.yml up django

django-celeryworker: ## celeryworker
	docker-compose -f develop.yml up celeryworker

django-celeryflower: ## celeryflower
	docker-compose -f develop.yml up celeryflower

django-mysql: ## mysql
	docker-compose -f develop.yml up mysql

redis-up: ## redis
	docker-compose -f develop.yml up redis

rabbitmq-up: ## redis
	docker-compose -f develop.yml up rabbitmq

shell: ## Enter Shell
	$(DJANGO_DOCKER_RUN) /bin/bash

dbshell: ## Enter mysql
	$(MYSQL_DOCKER_RUN) sh -c 'exec mysql -ujason -p123'

tmuxp: ## start tmuxp
	tmuxp load tmuxp.yml

sep--sep-b: ## ========== 测试与代码质量 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

lint: ## check style with flake8
	@echo "--> Linting python"
	flake8 django_blog
	@echo ""

sort: # sort import with isort
	@echo "--> Sort python imort"
	isort -rc .
	@echo ""


sep--sep-c: ## ========== 程序发布相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

dist: # builds source and wheel package
	python setup.py sdist bdist_wheel


sep--sep-d: ## ========== Docker 镜像相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

build-django: ## > base django
	docker build -t 'base-django:1.0' -f 'compose/django/Dockerfile' .

force-build-django: ## > base django
	docker build -t 'base-django:1.0' -f 'compose/django/Dockerfile' --no-cache .

build-all: build-django ## > build 所需所有镜像


sep--sep-e: ## ========== 文件清理相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

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
