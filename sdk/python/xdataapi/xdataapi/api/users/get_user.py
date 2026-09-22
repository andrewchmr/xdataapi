from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.user_response import UserResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    handle: str,
    *,
    fresh: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["fresh"] = fresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/users/{handle}".format(
            handle=quote(str(handle), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | UserResponse | None:
    if response.status_code == 200:
        response_200 = UserResponse.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404

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
) -> Response[Error | UserResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    handle: str,
    *,
    client: AuthenticatedClient | Client,
    fresh: bool | Unset = False,
) -> Response[Error | UserResponse]:
    """Profile by handle

     1 credit per profile.

    Args:
        handle (str):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UserResponse]
    """

    kwargs = _get_kwargs(
        handle=handle,
        fresh=fresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    handle: str,
    *,
    client: AuthenticatedClient | Client,
    fresh: bool | Unset = False,
) -> Error | UserResponse | None:
    """Profile by handle

     1 credit per profile.

    Args:
        handle (str):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UserResponse
    """

    return sync_detailed(
        handle=handle,
        client=client,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    handle: str,
    *,
    client: AuthenticatedClient | Client,
    fresh: bool | Unset = False,
) -> Response[Error | UserResponse]:
    """Profile by handle

     1 credit per profile.

    Args:
        handle (str):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UserResponse]
    """

    kwargs = _get_kwargs(
        handle=handle,
        fresh=fresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    handle: str,
    *,
    client: AuthenticatedClient | Client,
    fresh: bool | Unset = False,
) -> Error | UserResponse | None:
    """Profile by handle

     1 credit per profile.

    Args:
        handle (str):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UserResponse
    """

    return (
        await asyncio_detailed(
            handle=handle,
            client=client,
            fresh=fresh,
        )
    ).parsed
