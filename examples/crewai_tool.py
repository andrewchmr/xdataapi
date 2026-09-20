"""CrewAI tool over the xdataapi REST API. pip install crewai httpx"""
import os
import httpx
from crewai.tools import tool

BASE = "https://api.xdataapi.io"
HEADERS = {"x-api-key": os.environ["XDATAAPI_KEY"]}


@tool("Search X")
def search_x(q: str, count: int = 20) -> str:
    """Search public X (Twitter) posts with the x.com operators (from:, since:, min_faves:, lang:, "phrase")."""
    r = httpx.get(f"{BASE}/v1/tweets/search", params={"q": q, "count": count}, headers=HEADERS, timeout=30)
    return r.text


@tool("X profile")
def x_profile(handle: str) -> str:
    """Public profile of one X user by handle."""
    r = httpx.get(f"{BASE}/v1/users/{handle.lstrip('@')}", headers=HEADERS, timeout=30)
    return r.text
