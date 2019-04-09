.PHONY: install test dist

install:
	@pip install -r requirements_test.txt
	@pip install -e .

test:
	nosetests -s

dist:
	@python setup.py sdist upload
