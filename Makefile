.PHONY: install test dist

install:
	@pip install -r requirements_test.txt
	@pip install -e .

test:
	@nosetests -s --with-coverage --cover-inclusive --cover-package=dataset_manager

dist:
	@python setup.py sdist bdist_wheel
	@twine upload dist/*

