.PHONY: FORCE format build

main: format

format:
	black --line-length 78 src

build:
	pipenv run python -m build

upload:
	pipenv run python -m twine upload dist/*
