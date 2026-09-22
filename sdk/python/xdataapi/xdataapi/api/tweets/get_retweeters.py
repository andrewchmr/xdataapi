from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.user_page import UserPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    count: int | Unset = 50,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["count"] = count

    params["cursor"] = cursor

    params["fresh"] = fresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tweets/{id}/retweeters".format(
            id=quote(str(id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | UserPage | None:
    if response.status_code == 200:
        response_200 = UserPage.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401

    if response.status_code == 402:
        response_402 = Error.from_dict(response.json())

        return response_402

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())

        return response_403

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | UserPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 50,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Response[Error | UserPage]:
    """Accounts that retweeted a tweet

     0.5 credit per profile. Up to 200 per page. Not every reading session at X may read this; then the
    answer is 403 and free.

    Args:
        id (str):
        count (int | Unset):  Default: 50.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UserPage]
    """

    kwargs = _get_kwargs(
        id=id,
        count=count,
        cursor=cursor,
        fresh=fresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 50,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Error | UserPage | None:
    """Accounts that retweeted a tweet

     0.5 credit per profile. Up to 200 per page. Not every reading session at X may read this; then the
    answer is 403 and free.

    Args:
        id (str):
        count (int | Unset):  Default: 50.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UserPage
    """

    return sync_detailed(
        id=id,
        client=client,
        count=count,
        cursor=cursor,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 50,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Response[Error | UserPage]:
    """Accounts that retweeted a tweet

     0.5 credit per profile. Up to 200 per page. Not every reading session at X may read this; then the
    answer is 403 and free.

    Args:
        id (str):
        count (int | Unset):  Default: 50.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UserPage]
    """

    kwargs = _get_kwargs(
        id=id,
        count=count,
        cursor=cursor,
        fresh=fresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 50,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Error | UserPage | None:
    """Accounts that retweeted a tweet

     0.5 credit per profile. Up to 200 per page. Not every reading session at X may read this; then the
    answer is 403 and free.

    Args:
        id (str):
        count (int | Unset):  Default: 50.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UserPage
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            count=count,
            cursor=cursor,
            fresh=fresh,
        )
    ).parsed
