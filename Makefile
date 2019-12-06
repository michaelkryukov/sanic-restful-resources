all: test lint

test:
	python3 -m coverage run -m pytest -v
	python3 -m coverage report -m --fail-under=100 sanic_restful_resources.py

lint:
	python3 -m flake8 kutana/ --count --select=E9,F63,F7,F82 --show-source --statistics
	python3 -m flake8 kutana/ --count --max-complexity=10 --max-line-length=127 --statistics
