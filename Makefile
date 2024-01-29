.PHONY: help docs pubdocs update-requires
.DEFAULT_GOAL := help

help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'


docs: ## generate Sphinx HTML documentation, including API docs
	mkdir -p docs
	ls -A1 docs | xargs -I {} rm -rf docs/{}
	$(MAKE) -C docsrc clean html
	cp -a docsrc/_build/html/. docs

pubdocs: docs ## Publish the documentation to GitHub
	ghp-import -op docs


update-requires:  ## Update the requirements.txt file
	pip-compile --output-file=requirements/prod.txt pyproject.toml
	pip-compile --extra=test --output-file=requirements/test.txt pyproject.toml
	pip-compile --extra=docs --output-file=requirements/docs.txt pyproject.toml
	pip-compile --extra=dev --extra=docs --extra=test --output-file=requirements/dev.txt pyproject.toml
