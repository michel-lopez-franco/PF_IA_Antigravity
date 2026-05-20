.PHONY: check test nbval ci

check:
	mypy src/ --strict && ruff check src/ tests/

test:
	pytest tests/ --cov=src --cov-fail-under=80

nbval:
	pytest --nbval-lax cursos/

ci: check test nbval
