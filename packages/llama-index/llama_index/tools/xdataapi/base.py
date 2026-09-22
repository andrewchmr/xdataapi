"""LlamaIndex tool spec for xdataapi.io: read-only public X (Twitter) data.

Every method is a tool. The docstring is what the model reads, so each one says
what the call costs in credits.
"""

from __future__ import annotations

from typing import Any, List, Optional

from llama_index.core.tools.tool_spec.base import BaseToolSpec

from .client import XdataapiAuthError, XdataapiClient, XdataapiError

__all__ = ["XdataapiToolSpec", "XdataapiClient", "XdataapiError", "XdataapiAuthError"]


def _handle(value: str) -> str:
    return value.strip().lstrip("@")


class XdataapiToolSpec(BaseToolSpec):
    """Read public X (Twitter) data: profiles, posts, threads, followers, search.

    Read-only. No posting, no likes, no direct messages, no private data.

    Args:
        api_key: Key from https://xdataapi.io/dashboard. Read from
            ``XDATAAPI_KEY`` when not given.
        max_results: Ceiling on the page size of every paging tool, so one agent
            step cannot spend more than you allow.
    """

    spec_functions = [
        "search_tweets",
        "get_user",
        "get_users",
        "get_user_tweets",
        "get_tweet",
        "get_tweets",
        "get_thread",
        "get_replies",
        "get_quotes",
        "get_retweeters",
        "get_followers",
        "get_follower_ids",
        "get_following",
        "get_balance",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        max_results: Optional[int] = None,
        **client_kwargs: Any,
    ) -> None:
        self.client = XdataapiClient(api_key, max_results=max_results, **client_kwargs)

    # --- tweets ----------------------------------------------------------

    def search_tweets(
        self,
        q: str,
        product: Optional[str] = None,
        count: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> dict:
        """Search public X posts with the x.com operators.

        The entry point when you do not already know a handle or a post id.
        Costs 1 credit per result; an empty result is free.

        Args:
            q: x.com search syntax. Operators: from:handle, to:handle,
                since:YYYY-MM-DD, until:YYYY-MM-DD, min_faves:N, lang:xx,
                "exact phrase", OR, and - to exclude.
                Example: from:vercel since:2026-09-01 -filter:replies
            product: Latest (default, always available), Top (may answer 403,
                free), People (returns profiles), Photos, Videos.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            "/v1/tweets/search",
            {"q": q, "product": product, "count": self.client.cap(count), "cursor": cursor},
        )

    def get_tweet(self, id: str) -> dict:
        """Read one X post by numeric id, with its author. Costs 1 credit.

        Args:
            id: Numeric post id, as a string.
        """
        return self.client.get(f"/v1/tweets/{id}")

    def get_tweets(self, ids: List[str]) -> dict:
        """Read up to 100 X posts by id in ONE call.

        Prefer this over repeated single reads: one request, one rate-limit slot.
        Costs 1 credit per post found; deleted or private posts are listed in
        ``errors`` and cost nothing.

        Args:
            ids: Numeric post ids, at most 100.
        """
        return self.client.get("/v1/tweets/batch", {"ids": ",".join(str(i) for i in ids)})

    def get_thread(self, id: str, cursor: Optional[str] = None) -> dict:
        """Read one X post with its thread and replies, focal post first.

        Reads a whole conversation in one call. Costs 1 credit per post returned.

        Args:
            id: Numeric post id, as a string.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(f"/v1/tweets/{id}/thread", {"cursor": cursor})

    def get_replies(self, id: str, cursor: Optional[str] = None) -> dict:
        """Read the direct replies to one X post, one page. Costs 1 credit per reply.

        Args:
            id: Numeric post id, as a string.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(f"/v1/tweets/{id}/replies", {"cursor": cursor})

    def get_quotes(self, id: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the posts that quote one X post, newest first. Costs 1 credit per post.

        Args:
            id: Numeric post id, as a string.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/tweets/{id}/quotes", {"count": self.client.cap(count), "cursor": cursor}
        )

    def get_retweeters(self, id: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the accounts that reposted one X post. Costs 0.5 credit per profile.

        Some reading accounts are refused this by X; a 403 is free.

        Args:
            id: Numeric post id, as a string.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/tweets/{id}/retweeters", {"count": self.client.cap(count), "cursor": cursor}
        )

    # --- users -----------------------------------------------------------

    def get_user(self, handle: str) -> dict:
        """Read the public profile of one X user. Costs 1 credit.

        Args:
            handle: X handle, with or without the leading @.
        """
        return self.client.get(f"/v1/users/{_handle(handle)}")

    def get_users(self, handles: List[str]) -> dict:
        """Read up to 100 X profiles in ONE call.

        Prefer this over repeated single reads. Costs 1 credit per profile found;
        handles that do not exist are listed in ``errors`` and cost nothing.

        Args:
            handles: X handles, at most 100.
        """
        return self.client.get("/v1/users/batch", {"handles": ",".join(_handle(h) for h in handles)})

    def get_user_tweets(
        self, user: str, count: Optional[int] = None, cursor: Optional[str] = None
    ) -> dict:
        """Read the latest posts of one X user, newest first. Costs 1 credit per post.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_handle(user)}/tweets", {"count": self.client.cap(count), "cursor": cursor}
        )

    def get_followers(self, user: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the followers of an X user as full profiles. Costs 0.1 credit per profile.

        Use get_follower_ids when ids are enough: it costs five times less.
        Some reading accounts are refused this by X; a 403 is free.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_handle(user)}/followers", {"count": self.client.cap(count), "cursor": cursor}
        )

    def get_follower_ids(
        self, user: str, count: Optional[int] = None, cursor: Optional[str] = None
    ) -> dict:
        """Read the numeric ids of an X user's followers, without profiles.

        Costs 0.02 credit per id. Use it to size or intersect an audience.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_handle(user)}/followers/ids",
            {"count": self.client.cap(count), "cursor": cursor},
        )

    def get_following(self, user: str, count: Optional[int] = None, cursor: Optional[str] = None) -> dict:
        """Read the accounts an X user follows. Costs 0.1 credit per profile.

        Some reading accounts are refused this by X; a 403 is free.

        Args:
            user: X handle (with or without @) or numeric user id.
            count: Results on this page, 1 to 50.
            cursor: next_cursor from the previous page.
        """
        return self.client.get(
            f"/v1/users/{_handle(user)}/following", {"count": self.client.cap(count), "cursor": cursor}
        )

    # --- account ---------------------------------------------------------

    def get_balance(self) -> dict:
        """Read the credits left on this key and its rate limit. Free.

        Call it before a large read to check the budget covers the plan.
        """
        return self.client.get("/v1/me")
