# Contributing

## Getting started with development

### Setup

There are several ways to create your isolated environment. This is the default method.

Run the following in a terminal:

```console
# Clone the repository
git clone https://github.com/callowayproject/bump-my-version.git

# Enter the repository
cd bump-my-version

# Create then activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install the development requirements
python -m pip install -r requirements/dev.txt
```

### Run tests

Once setup, you should be able to run tests:

```console
pytest
```

## Install Pre-commit Hooks

Pre-commit hooks are scripts that run every time you make a commit. If any of the scripts fail, it stops the commit. You can see a listing of the checks in the ``.pre-commit-config.yaml`` file.

```console
pre-commit install
```
