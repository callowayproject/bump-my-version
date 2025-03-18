set export := true
set positional-arguments := true
set unstable
set script-interpreter := ['uv', 'run', '--script']

user := file_stem(home_directory())
curr_time := datetime("%Y.%m.%d-%H.%M.%S")

# Open the devenv shell
shell:
    {{ if env("DEVENV_RUNTIME", "") == "" { "sudo -E devenv shell --impure --verbose" } else { "echo 'Already in devenv shell!'" } }}

# Own the current directory as the logged in user
own:
    sudo chown -R {{ user }} .

# Bump the version of the package
bump type="" tag="false" dry="true":
    git add .
    BUMPVERSION_TAG={{ tag }} uv tool run bump-my-version bump {{ type }} --verbose {{ if dry == "true" { "--dry-run" } else { "" } }}

show-bump from-version="":
    uv tool run bump-my-version show-bump {{ from-version }}

get-version:
    uv tool run bump-my-version show current_version

# Initialize the python project environment
ready-py:
    uv lock
    uv sync --group dev --group test
    unset VIRTUAL_ENV

# Run the tests and open the coverage report
test:
    -pytest
    sudo -u {{ user }} gio open ./test-reports/htmlcov/index.html
