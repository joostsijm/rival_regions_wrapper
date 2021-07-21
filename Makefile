.PHONY: FORCE format

main: format

format:
	black --line-length 78 src
