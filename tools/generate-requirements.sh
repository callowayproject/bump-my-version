#!/usr/bin/env bash


pip-compile --output-file=requirements/prod.txt pyproject.toml
pip-compile --extra=docs --output-file=requirements/docs.txt pyproject.toml
pip-compile --extra=test --output-file=requirements/test.txt pyproject.toml
pip-compile --extra=dev --extra=docs --extra=test --output-file=requirements/dev.txt pyproject.toml
