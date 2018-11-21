MYSQL_DOCKER_RUN := docker exec -i -t django-blog_mysql_1
REDIS_DOCKER_RUN := docker exec -i -t django-blog_redis_1
WATCHDOG_RELOAD := watchmedo auto-restart --recursive -d . -p '*.py' --

## ========== 开发时命令 ==============

django-build-up: ## build and compose up
	docker-compose -f develop.yml up --build

django-down: ## build and compose up
	docker-compose -f develop.yml down

django-before-up: ## some deamons
	docker-compose -f develop.yml up -d redis mysql

django-runserver: ## runserver
	python manage.py runserver

django-celeryworker: ## celeryworker
	 $(WATCHDOG_RELOAD) celery -A django_blog.taskapp worker -l info

django-celeryflower: ## celeryflower
	celery -A django_blog.taskapp flower --port=5555

django-celerybeat: ## celerybeat
	$(WATCHDOG_RELOAD) celery -A django_blog.taskapp beat -s celerybeat-schedule

mysql-up: ## mysql
	docker-compose -f develop.yml up mysql

redis-up: ## redis
	docker-compose -f develop.yml up redis

rabbitmq-up: ## rabbitmq
	docker-compose -f develop.yml up rabbitmq

shell: ## Enter Shell
	./manage.py shell

dbshell: ## Enter mysql
	$(MYSQL_DOCKER_RUN) sh -c 'exec mysql -ujason -p123'

redis-cli: ## Enter mysql
	$(REDIS_DOCKER_RUN) sh -c 'redis-cli -a 123'

tmuxp: ## start tmuxp
	tmuxp load tmuxp.yml

## ========== 测试与代码质量 ==============

lint: ## check style with flake8
	@echo "--> Linting python"
	flake8 django_blog
	@echo ""

sort: # sort import with isort
	@echo "--> Sort python imort"
	isort -rc .
	@echo ""

sep--sep-b: ## ========== 文件清理相关 ==============
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


sep--sep-a: ## ========== 部署命令 ==============
deploy:	## deploy project
	@echo "--> Deploy project"
	fab -H tx -S ~/.ssh/config deploy