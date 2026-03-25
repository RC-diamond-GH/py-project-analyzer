.PHONY: test

test:
	poetry run pytest

deploy:
	pipx install --force .