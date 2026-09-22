# SDKs

Both packages are generated from `../openapi.yaml`; nothing in them is written by hand except the small
wrapper in `typescript/src/index.ts` and the READMEs. Run `./generate.sh` after an API change.

| Package | Registry | Path |
|---|---|---|
| `xdataapi` | npm | `typescript/` |
| `xdataapi` | PyPI | `python/xdataapi/` |

Publishing needs an npm and a PyPI account (`xdataapi` on both):
`cd typescript && npm publish --access public`, and `cd python/xdataapi && uv build && uv publish`.
