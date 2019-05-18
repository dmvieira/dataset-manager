.PHONY: install test dist version

install:
	@pip install -r requirements_test.txt
	@pip install -e .

test:
	nosetests -s --with-coverage --cover-inclusive --cover-package=dataset_manager

dist: version
	@git push --tags
	@git push origin HEAD
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@rm -rf dist/*

version:
	@echo Old Version
	@cat version.txt
	@echo
	@read -p "Enter New Version:" number; \
	echo "$$number" > version.txt; \
	git add version.txt; \
	git commit -m "Bump $$number"; \
	git tag $$number
