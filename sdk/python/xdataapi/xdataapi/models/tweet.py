from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.media import Media
    from ..models.user import User


T = TypeVar("T", bound="Tweet")


@_attrs_define
class Tweet:
    """
    Attributes:
        id (str):  Example: 20.
        text (str):
        created_at (datetime.datetime):
        author_id (str):
        lang (str | Unset):
        author (User | Unset):
        conversation_id (str | Unset):
        in_reply_to_id (str | Unset):
        in_reply_to_user_id (str | Unset):
        quoted_id (str | Unset):
        retweeted_id (str | Unset):
        replies (int | Unset):
        retweets (int | Unset):
        likes (int | Unset):
        quotes (int | Unset):
        bookmarks (int | Unset):
        views (int | Unset):
        media (list[Media] | Unset):
        urls (list[str] | Unset):
        hashtags (list[str] | Unset):
        mentions (list[str] | Unset):
        is_retweet (bool | Unset):
        is_quote (bool | Unset):
        is_reply (bool | Unset):
        source (str | Unset):
    """

    id: str
    text: str
    created_at: datetime.datetime
    author_id: str
    lang: str | Unset = UNSET
    author: User | Unset = UNSET
    conversation_id: str | Unset = UNSET
    in_reply_to_id: str | Unset = UNSET
    in_reply_to_user_id: str | Unset = UNSET
    quoted_id: str | Unset = UNSET
    retweeted_id: str | Unset = UNSET
    replies: int | Unset = UNSET
    retweets: int | Unset = UNSET
    likes: int | Unset = UNSET
    quotes: int | Unset = UNSET
    bookmarks: int | Unset = UNSET
    views: int | Unset = UNSET
    media: list[Media] | Unset = UNSET
    urls: list[str] | Unset = UNSET
    hashtags: list[str] | Unset = UNSET
    mentions: list[str] | Unset = UNSET
    is_retweet: bool | Unset = UNSET
    is_quote: bool | Unset = UNSET
    is_reply: bool | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        text = self.text

        created_at = self.created_at.isoformat()

        author_id = self.author_id

        lang = self.lang

        author: dict[str, Any] | Unset = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        conversation_id = self.conversation_id

        in_reply_to_id = self.in_reply_to_id

        in_reply_to_user_id = self.in_reply_to_user_id

        quoted_id = self.quoted_id

        retweeted_id = self.retweeted_id

        replies = self.replies

        retweets = self.retweets

        likes = self.likes

        quotes = self.quotes

        bookmarks = self.bookmarks

        views = self.views

        media: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.media, Unset):
            media = []
            for media_item_data in self.media:
                media_item = media_item_data.to_dict()
                media.append(media_item)

        urls: list[str] | Unset = UNSET
        if not isinstance(self.urls, Unset):
            urls = self.urls

        hashtags: list[str] | Unset = UNSET
        if not isinstance(self.hashtags, Unset):
            hashtags = self.hashtags

        mentions: list[str] | Unset = UNSET
        if not isinstance(self.mentions, Unset):
            mentions = self.mentions

        is_retweet = self.is_retweet

        is_quote = self.is_quote

        is_reply = self.is_reply

        source = self.source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "text": text,
                "created_at": created_at,
                "author_id": author_id,
            }
        )
        if lang is not UNSET:
            field_dict["lang"] = lang
        if author is not UNSET:
            field_dict["author"] = author
        if conversation_id is not UNSET:
            field_dict["conversation_id"] = conversation_id
        if in_reply_to_id is not UNSET:
            field_dict["in_reply_to_id"] = in_reply_to_id
        if in_reply_to_user_id is not UNSET:
            field_dict["in_reply_to_user_id"] = in_reply_to_user_id
        if quoted_id is not UNSET:
            field_dict["quoted_id"] = quoted_id
        if retweeted_id is not UNSET:
            field_dict["retweeted_id"] = retweeted_id
        if replies is not UNSET:
            field_dict["replies"] = replies
        if retweets is not UNSET:
            field_dict["retweets"] = retweets
        if likes is not UNSET:
            field_dict["likes"] = likes
        if quotes is not UNSET:
            field_dict["quotes"] = quotes
        if bookmarks is not UNSET:
            field_dict["bookmarks"] = bookmarks
        if views is not UNSET:
            field_dict["views"] = views
        if media is not UNSET:
            field_dict["media"] = media
        if urls is not UNSET:
            field_dict["urls"] = urls
        if hashtags is not UNSET:
            field_dict["hashtags"] = hashtags
        if mentions is not UNSET:
            field_dict["mentions"] = mentions
        if is_retweet is not UNSET:
            field_dict["is_retweet"] = is_retweet
        if is_quote is not UNSET:
            field_dict["is_quote"] = is_quote
        if is_reply is not UNSET:
            field_dict["is_reply"] = is_reply
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.media import Media  # noqa: PLC0415
        from ..models.user import User  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        text = d.pop("text")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        author_id = d.pop("author_id")

        lang = d.pop("lang", UNSET)

        _author = d.pop("author", UNSET)
        author: User | Unset
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = User.from_dict(_author)

        conversation_id = d.pop("conversation_id", UNSET)

        in_reply_to_id = d.pop("in_reply_to_id", UNSET)

        in_reply_to_user_id = d.pop("in_reply_to_user_id", UNSET)

        quoted_id = d.pop("quoted_id", UNSET)

        retweeted_id = d.pop("retweeted_id", UNSET)

        replies = d.pop("replies", UNSET)

        retweets = d.pop("retweets", UNSET)

        likes = d.pop("likes", UNSET)

        quotes = d.pop("quotes", UNSET)

        bookmarks = d.pop("bookmarks", UNSET)

        views = d.pop("views", UNSET)

        _media = d.pop("media", UNSET)
        media: list[Media] | Unset = UNSET
        if _media is not UNSET:
            media = []
            for media_item_data in _media:
                media_item = Media.from_dict(media_item_data)

                media.append(media_item)

        urls = cast(list[str], d.pop("urls", UNSET))

        hashtags = cast(list[str], d.pop("hashtags", UNSET))

        mentions = cast(list[str], d.pop("mentions", UNSET))

        is_retweet = d.pop("is_retweet", UNSET)

        is_quote = d.pop("is_quote", UNSET)

        is_reply = d.pop("is_reply", UNSET)

        source = d.pop("source", UNSET)

        tweet = cls(
            id=id,
            text=text,
            created_at=created_at,
            author_id=author_id,
            lang=lang,
            author=author,
            conversation_id=conversation_id,
            in_reply_to_id=in_reply_to_id,
            in_reply_to_user_id=in_reply_to_user_id,
            quoted_id=quoted_id,
            retweeted_id=retweeted_id,
            replies=replies,
            retweets=retweets,
            likes=likes,
            quotes=quotes,
            bookmarks=bookmarks,
            views=views,
            media=media,
            urls=urls,
            hashtags=hashtags,
            mentions=mentions,
            is_retweet=is_retweet,
            is_quote=is_quote,
            is_reply=is_reply,
            source=source,
        )

        tweet.additional_properties = d
        return tweet

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
