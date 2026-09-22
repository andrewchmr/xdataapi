from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.search_tweets_product import SearchTweetsProduct
from ...models.tweet_page import TweetPage
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    product: SearchTweetsProduct | Unset = SearchTweetsProduct.LATEST,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    json_product: str | Unset = UNSET
    if not isinstance(product, Unset):
        json_product = product.value

    params["product"] = json_product

    params["count"] = count

    params["cursor"] = cursor

    params["fresh"] = fresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tweets/search",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TweetPage | None:
    if response.status_code == 200:
        response_200 = TweetPage.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())

        return response_400

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | TweetPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    product: SearchTweetsProduct | Unset = SearchTweetsProduct.LATEST,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Response[Error | TweetPage]:
    """Advanced search

     1 credit per tweet, or per profile with `product=People` (then `data` is a list of User).
    `q` accepts X advanced search operators (from:, since:, until:, min_faves:, -filter:replies ...).
    `product=Top` is not served to every reading session at X; when it is not, the response is HTTP 403
    `product_unavailable` and nothing is charged. `Latest` is always available.

    Args:
        q (str):
        product (SearchTweetsProduct | Unset):  Default: SearchTweetsProduct.LATEST.
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
        q=q,
        product=product,
        count=count,
        cursor=cursor,
        fresh=fresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    product: SearchTweetsProduct | Unset = SearchTweetsProduct.LATEST,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Error | TweetPage | None:
    """Advanced search

     1 credit per tweet, or per profile with `product=People` (then `data` is a list of User).
    `q` accepts X advanced search operators (from:, since:, until:, min_faves:, -filter:replies ...).
    `product=Top` is not served to every reading session at X; when it is not, the response is HTTP 403
    `product_unavailable` and nothing is charged. `Latest` is always available.

    Args:
        q (str):
        product (SearchTweetsProduct | Unset):  Default: SearchTweetsProduct.LATEST.
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
        client=client,
        q=q,
        product=product,
        count=count,
        cursor=cursor,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    product: SearchTweetsProduct | Unset = SearchTweetsProduct.LATEST,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Response[Error | TweetPage]:
    """Advanced search

     1 credit per tweet, or per profile with `product=People` (then `data` is a list of User).
    `q` accepts X advanced search operators (from:, since:, until:, min_faves:, -filter:replies ...).
    `product=Top` is not served to every reading session at X; when it is not, the response is HTTP 403
    `product_unavailable` and nothing is charged. `Latest` is always available.

    Args:
        q (str):
        product (SearchTweetsProduct | Unset):  Default: SearchTweetsProduct.LATEST.
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
        q=q,
        product=product,
        count=count,
        cursor=cursor,
        fresh=fresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    product: SearchTweetsProduct | Unset = SearchTweetsProduct.LATEST,
    count: int | Unset = 20,
    cursor: str | Unset = UNSET,
    fresh: bool | Unset = False,
) -> Error | TweetPage | None:
    """Advanced search

     1 credit per tweet, or per profile with `product=People` (then `data` is a list of User).
    `q` accepts X advanced search operators (from:, since:, until:, min_faves:, -filter:replies ...).
    `product=Top` is not served to every reading session at X; when it is not, the response is HTTP 403
    `product_unavailable` and nothing is charged. `Latest` is always available.

    Args:
        q (str):
        product (SearchTweetsProduct | Unset):  Default: SearchTweetsProduct.LATEST.
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
            client=client,
            q=q,
            product=product,
            count=count,
            cursor=cursor,
            fresh=fresh,
        )
    ).parsed
