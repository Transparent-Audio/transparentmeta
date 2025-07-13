SOURCE=transparentmeta

.PHONY: checklist
checklist: reformat interrogate lint typehint test

.PHONY: clean
clean:
	find . -type f -name "*.pyc" | xargs rm -fr
	find . -type d -name __pycache__ | xargs rm -fr

.PHONY: install
install:
	poetry install --no-dev

.PHONY: install_dev
install_dev:
	poetry install
	poetry run pre-commit install

.PHONY: interrogate
interrogate:
	poetry run interrogate ${SOURCE} -c pyproject.toml -vv

.PHONY: lint
lint:
	poetry run pylint ${SOURCE}

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run

.PHONY: reformat
reformat:
	poetry run isort ${SOURCE} tests examples
	poetry run black ${SOURCE} tests examples

.PHONY: reformatdiff
reformatdiff:
	poetry run black --diff ${SOURCE}

.PHONY: test
test:
	poetry run pytest --cov-report term-missing --cov-report xml:coverage.xml --cov=${SOURCE}

.PHONY: typehint
typehint:
	poetry run mypy ${SOURCE}

.PHONY: loc
loc:
	cloc . --include-lang=Python --exclude-dir=tests

.PHONY: loc_with_tests
loc_with_tests:
	cloc . --include-lang=Python

.PHONY: start_docs
start_docs:
	poetry run sphinx-quickstart docs

.PHONY: build_docs
build_docs:
	poetry run sphinx-build -b html docs docs/_build/html

.PHONY: generate_api_docs
generate_api_docs:
	sphinx-apidoc -f -o docs/api/ transparentmeta/

.PHONY: tree
tree:
	tree -I '__pycache__|.venv|.git'
