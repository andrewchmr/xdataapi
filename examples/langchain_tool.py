"""LangChain tool over the xdataapi REST API. pip install langchain-core httpx

The tool returns the JSON the API returns, so the model sees credits_charged
and balance_remaining on every call and can stop when the balance is low.
"""
import os
import httpx
from langchain_core.tools import tool

BASE = "https://api.xdataapi.io"
HEADERS = {"x-api-key": os.environ["XDATAAPI_KEY"]}


@tool
def search_x(q: str, count: int = 20) -> dict:
    """Search public X (Twitter) posts. q takes the x.com operators:
    from:, to:, since:YYYY-MM-DD, until:, min_faves:, lang:, "phrase", OR, -."""
    r = httpx.get(f"{BASE}/v1/tweets/search", params={"q": q, "count": count}, headers=HEADERS, timeout=30)
    return r.json()


@tool
def x_profile(handle: str) -> dict:
    """Public profile of one X user by handle (with or without @)."""
    r = httpx.get(f"{BASE}/v1/users/{handle.lstrip('@')}", headers=HEADERS, timeout=30)
    return r.json()


@tool
def x_user_tweets(handle: str, count: int = 20) -> dict:
    """Latest posts of one X user, newest first."""
    r = httpx.get(f"{BASE}/v1/users/{handle.lstrip('@')}/tweets", params={"count": count}, headers=HEADERS, timeout=30)
    return r.json()


TOOLS = [search_x, x_profile, x_user_tweets]
