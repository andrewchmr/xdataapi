from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tweet_page import TweetPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user: str,
    *,
    count: int | Unset = 20,
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
        "url": "/v1/users/{user}/tweets".format(
            user=quote(str(user), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TweetPage | None:
    if response.status_code == 200:
        response_200 = TweetPage.from_dict(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | TweetPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Response[Error | TweetPage]:
    """Latest tweets of a user

     1 credit per tweet. `user` is a numeric id or a handle.

    Args:
        user (str):
        count (int | Unset):  Default: 20.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TweetPage]
    """

    kwargs = _get_kwargs(
        user=user,
        count=count,
        cursor=cursor,
        fresh=fresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Error | TweetPage | None:
    """Latest tweets of a user

     1 credit per tweet. `user` is a numeric id or a handle.

    Args:
        user (str):
        count (int | Unset):  Default: 20.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TweetPage
    """

    return sync_detailed(
        user=user,
        client=client,
        count=count,
        cursor=cursor,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    user: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Response[Error | TweetPage]:
    """Latest tweets of a user

     1 credit per tweet. `user` is a numeric id or a handle.

    Args:
        user (str):
        count (int | Unset):  Default: 20.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TweetPage]
    """

    kwargs = _get_kwargs(
        user=user,
        count=count,
        cursor=cursor,
        fresh=fresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user: str,
    *,
    client: AuthenticatedClient | Client,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Error | TweetPage | None:
    """Latest tweets of a user

     1 credit per tweet. `user` is a numeric id or a handle.

    Args:
        user (str):
        count (int | Unset):  Default: 20.
        cursor (str | Unset):
        fresh (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TweetPage
    """

    return (
        await asyncio_detailed(
            user=user,
            client=client,
            count=count,
            cursor=cursor,
            fresh=fresh,
        )
    ).parsed
