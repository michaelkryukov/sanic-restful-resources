all: test lint

test:
	python3 -m coverage run -m pytest -v
	python3 -m coverage report -m --fail-under=100 --include=sanic_restful_resources/*

lint:
	python3 -m flake8 --count --select=E9,F63,F7,F82 --show-source --statistics sanic_restful_resources/, examples/
	python3 -m flake8 --count --max-complexity=10 --max-line-length=127 --statistics sanic_restful_resources/, examples/
