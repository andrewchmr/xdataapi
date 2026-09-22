from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_tweets_body import GetTweetsBody
from ...models.tweet_batch import TweetBatch
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: GetTweetsBody,
    fresh: bool | Unset = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["fresh"] = fresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/tweets/batch",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | TweetBatch | None:
    if response.status_code == 200:
        response_200 = TweetBatch.from_dict(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | TweetBatch]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetTweetsBody,
    fresh: bool | Unset = False,
) -> Response[Error | TweetBatch]:
    """Tweets by id, batch

     Up to 100 tweets in one call. 1 credit per tweet found; deleted or private tweets are listed in
    `errors`
    and cost nothing. Results in input order. Also `GET /v1/tweets/batch?ids=20,21`.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TweetBatch]
    """

    kwargs = _get_kwargs(
        body=body,
        fresh=fresh,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: GetTweetsBody,
    fresh: bool | Unset = False,
) -> Error | TweetBatch | None:
    """Tweets by id, batch

     Up to 100 tweets in one call. 1 credit per tweet found; deleted or private tweets are listed in
    `errors`
    and cost nothing. Results in input order. Also `GET /v1/tweets/batch?ids=20,21`.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TweetBatch
    """

    return sync_detailed(
        client=client,
        body=body,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetTweetsBody,
    fresh: bool | Unset = False,
) -> Response[Error | TweetBatch]:
    """Tweets by id, batch

     Up to 100 tweets in one call. 1 credit per tweet found; deleted or private tweets are listed in
    `errors`
    and cost nothing. Results in input order. Also `GET /v1/tweets/batch?ids=20,21`.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | TweetBatch]
    """

    kwargs = _get_kwargs(
        body=body,
        fresh=fresh,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: GetTweetsBody,
    fresh: bool | Unset = False,
) -> Error | TweetBatch | None:
    """Tweets by id, batch

     Up to 100 tweets in one call. 1 credit per tweet found; deleted or private tweets are listed in
    `errors`
    and cost nothing. Results in input order. Also `GET /v1/tweets/batch?ids=20,21`.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetTweetsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | TweetBatch
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            fresh=fresh,
        )
    ).parsed
