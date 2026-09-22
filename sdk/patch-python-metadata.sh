#!/usr/bin/env bash
# openapi-python-client rewrites pyproject.toml on every run, and what it writes
# has no URLs at all. PyPI shows a package with no homepage as unattributed, and
# an agent checking whether a package is the official SDK for a domain has
# nothing to check against — which is exactly the question `sameAs` in our
# JSON-LD and the SDK docs page expect it to be able to answer.
#
# So: re-apply the metadata after every generation, idempotently.
set -euo pipefail
PY="$(cd "$(dirname "$0")" && pwd)/python/xdataapi/pyproject.toml"
[ -f "$PY" ] || { echo "no generated pyproject at $PY" >&2; exit 1; }

grep -q '^\[tool.poetry.urls\]' "$PY" && { echo "python metadata already present"; exit 0; }

python3 - "$PY" <<'PYEOF'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1])
s = p.read_text()

# Description and keywords, so a search for the product finds the package.
s = s.replace(
    'description = "A client library for accessing xdataapi.io API"',
    'description = "Python client for the xdataapi.io API: read-only X (Twitter) profiles, tweets, threads, search."',
)
if 'license =' not in s:
    s = s.replace('readme = "README.md"', 'license = "MIT"\nreadme = "README.md"\nhomepage = "https://xdataapi.io/docs/sdks"\nrepository = "https://github.com/xdataapi/xdataapi"\ndocumentation = "https://xdataapi.io/docs"\nkeywords = ["twitter", "x", "api", "tweets", "sdk", "xdataapi", "twitter-api", "x-api", "mcp", "agent", "llm"]')

urls = '''
[tool.poetry.urls]
Homepage = "https://xdataapi.io"
Documentation = "https://xdataapi.io/docs"
"API reference" = "https://xdataapi.io/reference"
"Source code" = "https://github.com/xdataapi/xdataapi"
"Issue tracker" = "https://github.com/xdataapi/xdataapi/issues"
'''
s = s.replace('\n[build-system]', urls + '\n[build-system]')
p.write_text(s)
print("python package metadata applied")
PYEOF
