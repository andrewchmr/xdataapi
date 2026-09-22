from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_checkout_body import CreateCheckoutBody
from ...models.create_checkout_response_200 import CreateCheckoutResponse200
from ...models.error import Error
from ...types import Response


def _get_kwargs(
    *,
    body: CreateCheckoutBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/billing/checkout",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateCheckoutResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = CreateCheckoutResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CreateCheckoutResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateCheckoutBody,
) -> Response[CreateCheckoutResponse200 | Error]:
    """Buy a credit pack

     Returns a Stripe Checkout URL. Open it in a browser; after payment the credits land in the wallet of
    the
    key's account within seconds. The rate limit follows the total paid over the account's life and only
    goes up (see `rate_limits` on `/v1/billing/packs`). Credits never expire.

    Args:
        body (CreateCheckoutBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateCheckoutResponse200 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: CreateCheckoutBody,
) -> CreateCheckoutResponse200 | Error | None:
    """Buy a credit pack

     Returns a Stripe Checkout URL. Open it in a browser; after payment the credits land in the wallet of
    the
    key's account within seconds. The rate limit follows the total paid over the account's life and only
    goes up (see `rate_limits` on `/v1/billing/packs`). Credits never expire.

    Args:
        body (CreateCheckoutBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateCheckoutResponse200 | Error
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: CreateCheckoutBody,
) -> Response[CreateCheckoutResponse200 | Error]:
    """Buy a credit pack

     Returns a Stripe Checkout URL. Open it in a browser; after payment the credits land in the wallet of
    the
    key's account within seconds. The rate limit follows the total paid over the account's life and only
    goes up (see `rate_limits` on `/v1/billing/packs`). Credits never expire.

    Args:
        body (CreateCheckoutBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateCheckoutResponse200 | Error]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: CreateCheckoutBody,
) -> CreateCheckoutResponse200 | Error | None:
    """Buy a credit pack

     Returns a Stripe Checkout URL. Open it in a browser; after payment the credits land in the wallet of
    the
    key's account within seconds. The rate limit follows the total paid over the account's life and only
    goes up (see `rate_limits` on `/v1/billing/packs`). Credits never expire.

    Args:
        body (CreateCheckoutBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateCheckoutResponse200 | Error
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
