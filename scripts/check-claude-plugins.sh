#!/usr/bin/env bash
# Validate the Claude marketplace and every category native plugin manifest.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v claude >/dev/null 2>&1; then
  echo "FAIL: claude CLI is required for Claude plugin validation"
  exit 1
fi

status=0
marketplace=".claude-plugin/marketplace.json"

if [ ! -f "$marketplace" ]; then
  echo "FAIL: $marketplace is required"
  exit 1
fi

echo "Validating Claude marketplace: $marketplace"
if ! claude plugin validate --strict "$marketplace"; then
  status=1
fi

expected=0
validated=0

for category in plugins/*; do
  [ -d "$category" ] || continue
  expected=$((expected + 1))
  manifest="$category/.claude-plugin/plugin.json"
  if [ ! -f "$manifest" ]; then
    echo "FAIL: missing Claude manifest: $manifest"
    status=1
    continue
  fi
  echo "Validating Claude plugin manifest: $manifest"
  if ! claude plugin validate --strict "$manifest"; then
    status=1
  else
    validated=$((validated + 1))
  fi
done

if [ "$expected" -eq 0 ]; then
  echo "FAIL: plugins/ must contain at least one category"
  exit 1
fi

if [ "$validated" -ne "$expected" ]; then
  echo "FAIL: validated $validated Claude category manifests, expected exactly $expected"
  status=1
fi

if [ "$status" -eq 0 ]; then
  echo "OK: Claude marketplace and $validated category manifests validated"
fi
exit "$status"
