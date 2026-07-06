#!/usr/bin/env bash
#
# Sync the public mirror from this (private) repo, PRESERVING full commit
# history while removing every `_files/` directory from all commits.
#
# How it works: a fresh throwaway clone of the private repo is rewritten with
# git-filter-repo (run via `uvx`, so nothing needs to be installed) to strip
# `_files/` out of every commit, then force-pushed to the public remote.
# Because history is rewritten, this is a force-push and the public commit SHAs
# will differ from the private ones. Commits that only ever touched `_files/`
# become empty and are pruned from the public history.
#
# Workflow: commit your work on the private repo, then run this script.
#
# Usage:   ./sync-public.sh
# Config:  BRANCH         (default: master)
#          PUBLIC_URL     (default: https://github.com/ryn-cx/chirashi.git)
#          EXCLUDE_REGEX  (default: (?:^|/)_files/  -- paths stripped from public)
#          PUSH_TAGS      (set to 1 to also force-push tags)

set -euo pipefail

BRANCH="${BRANCH:-master}"
PUBLIC_URL="${PUBLIC_URL:-https://github.com/ryn-cx/chirashi.git}"
EXCLUDE_REGEX="${EXCLUDE_REGEX:-(?:^|/)_files/}"
PUSH_TAGS="${PUSH_TAGS:-0}"

PRIVATE_ROOT="$(git rev-parse --show-toplevel)"

TMP="$(mktemp -d)"
cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

echo "Cloning '$BRANCH' into a scratch workspace..."
# --no-local forces a real (non-hardlinked) clone so filter-repo has a clean repo.
git clone --no-local --single-branch --branch "$BRANCH" "$PRIVATE_ROOT" "$TMP/work"

echo "Rewriting history to remove paths matching /$EXCLUDE_REGEX/ ..."
# The default regex '(?:^|/)_files/' matches any path with an exact `_files`
# directory segment, at any depth; --invert-paths removes those paths from every
# commit. (Use a non-capturing group: filter-repo does not honor '(^|/)'.)
( cd "$TMP/work" && uvx git-filter-repo --force --invert-paths --path-regex "$EXCLUDE_REGEX" )

echo "Force-pushing rewritten '$BRANCH' to public ($PUBLIC_URL) ..."
git -C "$TMP/work" push --force "$PUBLIC_URL" "HEAD:refs/heads/$BRANCH"

if [ "$PUSH_TAGS" = "1" ]; then
  echo "Force-pushing tags ..."
  git -C "$TMP/work" push --force --tags "$PUBLIC_URL"
fi

echo "Done: public '$BRANCH' now mirrors private history without _files."
