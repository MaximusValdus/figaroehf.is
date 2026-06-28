.PHONY: help install install-dev init-db test brief serve clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install:  ## Install runtime dependencies
	pip install -r requirements.txt

install-dev:  ## Install runtime + test dependencies
	pip install -r requirements-dev.txt

init-db:  ## Create the SQLite tables
	python -m assistant.cli init-db

test:  ## Run the test suite
	python -m pytest

brief:  ## Generate today's daily brief
	python -m assistant.cli brief

serve:  ## Run the FastAPI server
	python -m assistant.cli serve

clean:  ## Remove caches and local databases
	rm -rf .pytest_cache **/__pycache__ *.db
