"""HTTP client for the xdataapi.io REST API.

The tools hand the model the JSON the API returns, unchanged, so it sees
``credits_charged`` and ``balance_remaining`` on every call and can stop before
the balance runs out.
"""

from __future__ import annotations

import os
from typing import Any, Mapping

import httpx

BASE_URL = "https://api.xdataapi.io"

#: Failures the model can act on: try another handle, ask for a smaller page,
#: tell the user the balance is empty. These come back as data.
_REPORTED = frozenset({400, 402, 403, 404})


class XdataapiError(RuntimeError):
    """A call failed in a way the model cannot repair."""

    def __init__(self, message: str, *, code: str = "", status: int = 0, request_id: str = "") -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.request_id = request_id


class XdataapiAuthError(XdataapiError):
    """The key is missing, unknown or revoked. A configuration fault."""


def _problem(response: httpx.Response) -> dict[str, Any]:
    try:
        body = response.json()
    except ValueError:
        body = {}
    return body if isinstance(body, dict) else {}


class XdataapiClient:
    """Thin wrapper over the REST API. Sync and async, one key.

    Args:
        api_key: Key from https://xdataapi.io/dashboard. Read from
            ``XDATAAPI_KEY`` when not given.
        base_url: Override for testing or for a private deployment.
        timeout: Seconds per request.
        max_results: Ceiling on ``count`` for every paging tool. Set it to cap
            what one agent step can spend. ``None`` leaves the API default.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_results: int | None = None,
        client: httpx.Client | None = None,
        async_client: httpx.AsyncClient | None = None,
    ) -> None:
        key = api_key or os.environ.get("XDATAAPI_KEY")
        if not key:
            raise XdataapiAuthError(
                "No API key. Pass api_key=... or set XDATAAPI_KEY. "
                "Get one at https://xdataapi.io/dashboard."
            )
        self.api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_results = max_results
        self._client = client
        self._async_client = async_client

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "accept": "application/json",
            "user-agent": "llama-index-tools-xdataapi",
        }

    def cap(self, count: int | None) -> int | None:
        """Apply ``max_results`` to a requested page size."""
        if count is None:
            return self.max_results
        if self.max_results is None:
            return count
        return min(count, self.max_results)

    def _handle(self, response: httpx.Response) -> dict[str, Any]:
        if response.status_code < 400:
            return _problem(response)

        body = _problem(response)
        error = body.get("error") or {}
        code = str(error.get("code") or "")
        message = str(error.get("message") or response.reason_phrase or "request failed")
        request_id = str(body.get("request_id") or "")

        if response.status_code == 401:
            raise XdataapiAuthError(
                f"{message} (code {code or 'invalid_key'}). "
                "Check XDATAAPI_KEY against https://xdataapi.io/dashboard.",
                code=code,
                status=401,
                request_id=request_id,
            )
        if response.status_code in _REPORTED:
            # Nothing was charged for these. Let the model read and decide.
            return body
        raise XdataapiError(
            f"{message} (HTTP {response.status_code}, code {code}, request {request_id})",
            code=code,
            status=response.status_code,
            request_id=request_id,
        )

    @staticmethod
    def _clean(params: Mapping[str, Any] | None) -> dict[str, Any]:
        return {k: v for k, v in (params or {}).items() if v is not None}

    def get(self, path: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        client = self._client
        if client is None:
            with httpx.Client(timeout=self.timeout) as fresh:
                return self._handle(
                    fresh.get(f"{self.base_url}{path}", params=self._clean(params), headers=self._headers)
                )
        return self._handle(
            client.get(f"{self.base_url}{path}", params=self._clean(params), headers=self._headers)
        )

    async def aget(self, path: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
        client = self._async_client
        if client is None:
            async with httpx.AsyncClient(timeout=self.timeout) as fresh:
                return self._handle(
                    await fresh.get(
                        f"{self.base_url}{path}", params=self._clean(params), headers=self._headers
                    )
                )
        return self._handle(
            await client.get(f"{self.base_url}{path}", params=self._clean(params), headers=self._headers)
        )
