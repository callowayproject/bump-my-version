#!/usr/bin/env bash


function extract_version_content() {
  changelog=$1
  target_version=$2

  awk -v target="$target_version" '
    /^## / {
      if (found) exit;
      version=$2;
      if (version == target) found=1;
      next;
    }
    found { print; }
  ' <<< "$changelog"
}

changelog=$(cat "CHANGELOG.md")
TARGET_VERSION=$(bump-my-version show current_version)
NOTES=$(extract_version_content "$changelog" "$TARGET_VERSION")
echo "Creating a GitHub release for version ${TARGET_VERSION} with notes."
gh release create \
  "${TARGET_VERSION}" \
  ./dist/* \
  --title "${TARGET_VERSION}" \
  --notes "${NOTES}" \
  --draft
