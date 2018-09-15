lint: ## check style with flake8
	@echo "--> Linting python"
	flake8 django_blog tests
	@echo ""

sort: # sort import with isort
	@echo "--> Sort python imort"
	isort -rc .
	@echo ""

package:
	python setup.py sdist bdist_wheel

clean:
	@echo "--> Cleaning package data"
	rm -rf dist/* build/*
	@echo "--> Cleaning pyc files"
	find . -name "*.pyc" -delete
	@echo ""
