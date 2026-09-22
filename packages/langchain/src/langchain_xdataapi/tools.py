"""LangChain tools over the xdataapi.io read endpoints.

Every tool is read-only. The credit cost is written into each description, so a
model that plans a multi-step read knows what the plan costs before it runs it.
"""

from __future__ import annotations

import json
from typing import Any, Literal, Sequence

from langchain_core.callbacks import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field

from .client import XdataapiClient


def _handle(value: str) -> str:
    return value.strip().lstrip("@")


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


class _Base(BaseTool):
    """Shared plumbing: one client, JSON in and JSON out."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    client: XdataapiClient
    response_format: str = "content"

    def _call(self, **kwargs: Any) -> tuple[str, dict[str, Any] | None]:
        raise NotImplementedError

    def _run(self, run_manager: CallbackManagerForToolRun | None = None, **kwargs: Any) -> str:
        path, params = self._call(**kwargs)
        return _dump(self.client.get(path, params))

    async def _arun(self, run_manager: AsyncCallbackManagerForToolRun | None = None, **kwargs: Any) -> str:
        path, params = self._call(**kwargs)
        return _dump(await self.client.aget(path, params))


# --- users ---------------------------------------------------------------


class _UserArgs(BaseModel):
    handle: str = Field(description="X handle, with or without the leading @.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetUser(_Base):
    name: str = "x_get_user"
    description: str = (
        "Public profile of one X (Twitter) user by handle: bio, counts, verified state, "
        "created date. Costs 1 credit."
    )
    args_schema: type[BaseModel] = _UserArgs

    def _call(self, handle: str, fresh: bool | None = None) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/users/{_handle(handle)}", {"fresh": fresh}


class _UsersArgs(BaseModel):
    handles: Sequence[str] = Field(description="Up to 100 handles in one call.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetUsers(_Base):
    name: str = "x_get_users"
    description: str = (
        "Profiles of up to 100 X users in ONE call. Prefer this over repeated single reads: "
        "it is one request and one rate-limit slot. Costs 1 credit per profile found; "
        "handles that do not exist are listed in errors and cost nothing."
    )
    args_schema: type[BaseModel] = _UsersArgs

    def _call(self, handles: Sequence[str], fresh: bool | None = None) -> tuple[str, dict[str, Any] | None]:
        return "/v1/users/batch", {"handles": ",".join(_handle(h) for h in handles), "fresh": fresh}


class _PageArgs(BaseModel):
    user: str = Field(description="X handle (with or without @) or numeric user id.")
    count: int | None = Field(default=None, description="Results on this page. 1 to 50.")
    cursor: str | None = Field(default=None, description="next_cursor from the previous page.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetUserTweets(_Base):
    name: str = "x_get_user_tweets"
    description: str = (
        "Latest posts of one X user, newest first. Pages with next_cursor. Costs 1 credit per post."
    )
    args_schema: type[BaseModel] = _PageArgs

    def _call(
        self, user: str, count: int | None = None, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/users/{_handle(user)}/tweets", {
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


class GetFollowers(_Base):
    name: str = "x_get_followers"
    description: str = (
        "Followers of an X user, as full profiles. Costs 0.1 credit per profile. "
        "Some accounts refuse this read; a 403 is free. Use x_get_follower_ids when ids are enough."
    )
    args_schema: type[BaseModel] = _PageArgs

    def _call(
        self, user: str, count: int | None = None, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/users/{_handle(user)}/followers", {
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


class GetFollowerIds(_Base):
    name: str = "x_get_follower_ids"
    description: str = (
        "Numeric ids of an X user's followers, without the profiles. Costs 0.02 credit per id, "
        "five times less than x_get_followers. Use it to size or intersect an audience."
    )
    args_schema: type[BaseModel] = _PageArgs

    def _call(
        self, user: str, count: int | None = None, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/users/{_handle(user)}/followers/ids", {
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


class GetFollowing(_Base):
    name: str = "x_get_following"
    description: str = (
        "Accounts an X user follows. Costs 0.1 credit per profile. Some accounts refuse this read; "
        "a 403 is free."
    )
    args_schema: type[BaseModel] = _PageArgs

    def _call(
        self, user: str, count: int | None = None, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/users/{_handle(user)}/following", {
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


# --- tweets --------------------------------------------------------------


class _SearchArgs(BaseModel):
    q: str = Field(
        description=(
            "Query in x.com search syntax. Operators: from:handle, to:handle, since:YYYY-MM-DD, "
            'until:YYYY-MM-DD, min_faves:N, lang:xx, "exact phrase", OR, and - to exclude. '
            'Example: from:vercel since:2026-09-01 -filter:replies'
        )
    )
    product: Literal["Latest", "Top", "People", "Photos", "Videos"] | None = Field(
        default=None,
        description=(
            "Latest (default, always available), Top (may answer 403, free), People (returns "
            "profiles), Photos, Videos."
        ),
    )
    count: int | None = Field(default=None, description="Results on this page. 1 to 50.")
    cursor: str | None = Field(default=None, description="next_cursor from the previous page.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class SearchTweets(_Base):
    name: str = "x_search_tweets"
    description: str = (
        "Search public X posts with the x.com operators. The main entry point when you do not "
        "already know a handle or a post id. Costs 1 credit per result returned; an empty result "
        "is free. Pages with next_cursor."
    )
    args_schema: type[BaseModel] = _SearchArgs

    def _call(
        self,
        q: str,
        product: str | None = None,
        count: int | None = None,
        cursor: str | None = None,
        fresh: bool | None = None,
    ) -> tuple[str, dict[str, Any] | None]:
        return "/v1/tweets/search", {
            "q": q,
            "product": product,
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


class _TweetArgs(BaseModel):
    id: str = Field(description="Numeric post id, as a string.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetTweet(_Base):
    name: str = "x_get_tweet"
    description: str = "One X post by numeric id, with its author. Costs 1 credit."
    args_schema: type[BaseModel] = _TweetArgs

    def _call(self, id: str, fresh: bool | None = None) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/tweets/{id}", {"fresh": fresh}


class _TweetsArgs(BaseModel):
    ids: Sequence[str] = Field(description="Up to 100 numeric post ids in one call.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetTweets(_Base):
    name: str = "x_get_tweets"
    description: str = (
        "Up to 100 X posts by id in ONE call. Prefer this over repeated single reads. "
        "Costs 1 credit per post found; deleted or private posts are listed in errors and cost nothing."
    )
    args_schema: type[BaseModel] = _TweetsArgs

    def _call(self, ids: Sequence[str], fresh: bool | None = None) -> tuple[str, dict[str, Any] | None]:
        return "/v1/tweets/batch", {"ids": ",".join(str(i) for i in ids), "fresh": fresh}


class _ThreadArgs(BaseModel):
    id: str = Field(description="Numeric post id, as a string.")
    cursor: str | None = Field(default=None, description="next_cursor from the previous page.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetThread(_Base):
    name: str = "x_get_thread"
    description: str = (
        "One X post with its thread and replies, the focal post first. Use it to read a whole "
        "conversation in one call. Costs 1 credit per post returned."
    )
    args_schema: type[BaseModel] = _ThreadArgs

    def _call(
        self, id: str, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/tweets/{id}/thread", {"cursor": cursor, "fresh": fresh}


class GetReplies(_Base):
    name: str = "x_get_replies"
    description: str = "Direct replies to one X post, one page. Costs 1 credit per reply."
    args_schema: type[BaseModel] = _ThreadArgs

    def _call(
        self, id: str, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/tweets/{id}/replies", {"cursor": cursor, "fresh": fresh}


class _CountedTweetArgs(BaseModel):
    id: str = Field(description="Numeric post id, as a string.")
    count: int | None = Field(default=None, description="Results on this page. 1 to 50.")
    cursor: str | None = Field(default=None, description="next_cursor from the previous page.")
    fresh: bool | None = Field(default=None, description="Skip the cache. Costs double.")


class GetQuotes(_Base):
    name: str = "x_get_quotes"
    description: str = "Posts that quote one X post, newest first. Costs 1 credit per post."
    args_schema: type[BaseModel] = _CountedTweetArgs

    def _call(
        self, id: str, count: int | None = None, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/tweets/{id}/quotes", {
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


class GetRetweeters(_Base):
    name: str = "x_get_retweeters"
    description: str = (
        "Accounts that reposted one X post. Costs 0.5 credit per profile. Some accounts refuse "
        "this read; a 403 is free."
    )
    args_schema: type[BaseModel] = _CountedTweetArgs

    def _call(
        self, id: str, count: int | None = None, cursor: str | None = None, fresh: bool | None = None
    ) -> tuple[str, dict[str, Any] | None]:
        return f"/v1/tweets/{id}/retweeters", {
            "count": self.client.cap(count),
            "cursor": cursor,
            "fresh": fresh,
        }


# --- account -------------------------------------------------------------


class _NoArgs(BaseModel):
    pass


class GetBalance(_Base):
    name: str = "x_get_balance"
    description: str = (
        "Credits left on this key and its rate limit. Free. Call it before a large read to check "
        "the budget covers the plan."
    )
    args_schema: type[BaseModel] = _NoArgs

    def _call(self) -> tuple[str, dict[str, Any] | None]:
        return "/v1/me", None


ALL_TOOLS: tuple[type[_Base], ...] = (
    SearchTweets,
    GetUser,
    GetUsers,
    GetUserTweets,
    GetTweet,
    GetTweets,
    GetThread,
    GetReplies,
    GetQuotes,
    GetRetweeters,
    GetFollowers,
    GetFollowerIds,
    GetFollowing,
    GetBalance,
)
