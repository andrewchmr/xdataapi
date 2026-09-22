#!/usr/bin/env bash
# Regenerate both SDKs from openapi.yaml. Run after every API change; commit the output.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
echo "== typescript"
(cd "$HERE/typescript" && pnpm install --frozen-lockfile >/dev/null && rm -rf src/generated && pnpm generate >/dev/null && pnpm build >/dev/null)
echo "== python"
(cd "$HERE/python" && rm -rf xdataapi && uv tool run --from openapi-python-client openapi-python-client generate \
  --path ../../openapi.yaml --config config.yaml --output-path xdataapi --overwrite >/dev/null)
# The generator rewrites pyproject.toml every time and writes no URLs; put the
# package's identity back before it is built, or PyPI publishes an SDK that
# cannot be tied to the domain it is the SDK for.
"$HERE/patch-python-metadata.sh"
(cd "$HERE/python/xdataapi" && uv build >/dev/null 2>&1 && rm -rf dist)
echo "ok"
