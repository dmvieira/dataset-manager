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

version:
	@echo Old Version
	@cat dataset_manager/__version__.py
	@echo
	@read -p "Enter New Version:" number; \
	echo "number = '$$number'" > dataset_manager/__version__.py; \
	git add dataset_manager/__version__.py; \
	git commit -m "Bump $$number"; \
	git tag $$number
