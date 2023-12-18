#!/usr/bin/env bash

rm -Rf dist
RELEASE_KIND=$(generate-changelog --output release-hint)
echo "::notice::Suggested release type is: ${RELEASE_KIND}"
PR_NUMBER=$(gh pr view --json number -q .number || echo "")
echo "::notice::PR number is: ${PR_NUMBER}"
REVISION=$(git describe --tags --long | awk -F- '{print $2}')
echo "::notice::Revision is: ${REVISION}"
export PR_NUMBER REVISION
bump-my-version bump -v $RELEASE_KIND
python -m build
python -m twine upload dist/*
