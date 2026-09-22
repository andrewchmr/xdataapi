# xdataapi (Python)

Typed Python client for [xdataapi.io](https://xdataapi.io), the read-only X (Twitter) data API.
Generated from the API's OpenAPI document with `openapi-python-client`; the package lives in `xdataapi/`.

```bash
pip install xdataapi
```

```python
from xdataapi import AuthenticatedClient
from xdataapi.api.users import get_user, get_users
from xdataapi.api.tweets import search_tweets
from xdataapi.models import GetUsersBody

client = AuthenticatedClient(
    base_url="https://api.xdataapi.io",
    token=os.environ["XDATAAPI_KEY"],
    prefix="",
    auth_header_name="x-api-key",
)

profile = get_user.sync(client=client, handle="x")
print(profile.data.followers, profile.credits_charged)

page = search_tweets.sync(client=client, q="from:x since:2026-09-01", count=20)
for t in page.data:
    print(t.id, t.text)

many = get_users.sync(client=client, body=GetUsersBody(handles=["x", "github", "vercel"]))
print(many.items, many.errors)
```

Each operation module has `sync`, `sync_detailed`, `asyncio` and `asyncio_detailed`. The `_detailed` forms
return the status code and headers too; the plain forms return the parsed body, or an `Error` model on a
non-2xx status. Pagination: pass `next_cursor` from a page back as `cursor`.

Docs: https://xdataapi.io/docs. API reference: https://xdataapi.io/reference.

## Regenerate

```bash
cd sdk/python && uv tool run --from openapi-python-client openapi-python-client generate \
  --path ../../openapi.yaml --config config.yaml --output-path xdataapi --overwrite
```
