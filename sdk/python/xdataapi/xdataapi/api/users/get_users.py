from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.get_users_body import GetUsersBody
from ...models.user_batch import UserBatch
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: GetUsersBody,
    fresh: bool | Unset = False,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["fresh"] = fresh

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/users/batch",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | UserBatch | None:
    if response.status_code == 200:
        response_200 = UserBatch.from_dict(response.json())

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | UserBatch]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetUsersBody,
    fresh: bool | Unset = False,
) -> Response[Error | UserBatch]:
    """Profiles by handle, batch

     Up to 100 profiles in one call. 1 credit per profile found; handles that do not exist are listed in
    `errors` and cost nothing. Duplicates are folded. Results in input order. Also `GET
    /v1/users/batch?handles=a,b,c`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UserBatch]
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
    body: GetUsersBody,
    fresh: bool | Unset = False,
) -> Error | UserBatch | None:
    """Profiles by handle, batch

     Up to 100 profiles in one call. 1 credit per profile found; handles that do not exist are listed in
    `errors` and cost nothing. Duplicates are folded. Results in input order. Also `GET
    /v1/users/batch?handles=a,b,c`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UserBatch
    """

    return sync_detailed(
        client=client,
        body=body,
        fresh=fresh,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: GetUsersBody,
    fresh: bool | Unset = False,
) -> Response[Error | UserBatch]:
    """Profiles by handle, batch

     Up to 100 profiles in one call. 1 credit per profile found; handles that do not exist are listed in
    `errors` and cost nothing. Duplicates are folded. Results in input order. Also `GET
    /v1/users/batch?handles=a,b,c`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UserBatch]
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
    body: GetUsersBody,
    fresh: bool | Unset = False,
) -> Error | UserBatch | None:
    """Profiles by handle, batch

     Up to 100 profiles in one call. 1 credit per profile found; handles that do not exist are listed in
    `errors` and cost nothing. Duplicates are folded. Results in input order. Also `GET
    /v1/users/batch?handles=a,b,c`.
    When the balance covers only part of the list, the tail comes back as `no_credits` and is not
    fetched.

    Args:
        fresh (bool | Unset):  Default: False.
        body (GetUsersBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UserBatch
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            fresh=fresh,
        )
    ).parsed
