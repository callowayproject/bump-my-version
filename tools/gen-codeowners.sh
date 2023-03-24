#!/usr/bin/env bash

# Generate the CODEOWNERS file for all unempty files
#
# Requires git-fame: pip install git-fame
#
# Usage: gen-codeowners.sh path1 [path2 ...]

owners(){
  for f in $(git ls-files "$*"); do
    LINECOUNT=$(wc -l "$f" | awk '{print $1}')
    if [[ $LINECOUNT -gt 0 ]]; then
      echo -n "$f "
      # author emails if loc distribution >= 30%
      git fame -esnwMC --incl "$f" | tr '/' '|' \
        | awk -v filename="$f" -F '|' '(NR>6 && $6>=30) {print $2}' \
        | xargs echo
    fi
  done
}
owners "$*" | tee CODEOWNERS
