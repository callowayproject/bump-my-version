#!/usr/bin/env bash


pip-compile --upgrade --output-file=requirements/prod.txt pyproject.toml
pip-compile --upgrade --extra=docs --output-file=requirements/docs.txt pyproject.toml
pip-compile --upgrade --extra=test --output-file=requirements/test.txt pyproject.toml
pip-compile --upgrade --extra=dev --extra=docs --extra=test --output-file=requirements/dev.txt pyproject.toml
