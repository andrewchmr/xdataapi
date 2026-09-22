from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        id (str):  Example: 783214.
        handle (str):  Example: X.
        name (str):
        followers (int):
        following (int):
        tweets (int):
        created_at (datetime.datetime):
        bio (str | Unset):
        location (str | Unset):
        url (str | Unset):
        avatar_url (str | Unset):
        banner_url (str | Unset):
        verified (bool | Unset):
        protected (bool | Unset):
        likes (int | Unset):
        listed (int | Unset):
        pinned_tweet_ids (list[str] | Unset):
    """

    id: str
    handle: str
    name: str
    followers: int
    following: int
    tweets: int
    created_at: datetime.datetime
    bio: str | Unset = UNSET
    location: str | Unset = UNSET
    url: str | Unset = UNSET
    avatar_url: str | Unset = UNSET
    banner_url: str | Unset = UNSET
    verified: bool | Unset = UNSET
    protected: bool | Unset = UNSET
    likes: int | Unset = UNSET
    listed: int | Unset = UNSET
    pinned_tweet_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        handle = self.handle

        name = self.name

        followers = self.followers

        following = self.following

        tweets = self.tweets

        created_at = self.created_at.isoformat()

        bio = self.bio

        location = self.location

        url = self.url

        avatar_url = self.avatar_url

        banner_url = self.banner_url

        verified = self.verified

        protected = self.protected

        likes = self.likes

        listed = self.listed

        pinned_tweet_ids: list[str] | Unset = UNSET
        if not isinstance(self.pinned_tweet_ids, Unset):
            pinned_tweet_ids = self.pinned_tweet_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "handle": handle,
                "name": name,
                "followers": followers,
                "following": following,
                "tweets": tweets,
                "created_at": created_at,
            }
        )
        if bio is not UNSET:
            field_dict["bio"] = bio
        if location is not UNSET:
            field_dict["location"] = location
        if url is not UNSET:
            field_dict["url"] = url
        if avatar_url is not UNSET:
            field_dict["avatar_url"] = avatar_url
        if banner_url is not UNSET:
            field_dict["banner_url"] = banner_url
        if verified is not UNSET:
            field_dict["verified"] = verified
        if protected is not UNSET:
            field_dict["protected"] = protected
        if likes is not UNSET:
            field_dict["likes"] = likes
        if listed is not UNSET:
            field_dict["listed"] = listed
        if pinned_tweet_ids is not UNSET:
            field_dict["pinned_tweet_ids"] = pinned_tweet_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        handle = d.pop("handle")

        name = d.pop("name")

        followers = d.pop("followers")

        following = d.pop("following")

        tweets = d.pop("tweets")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))

        bio = d.pop("bio", UNSET)

        location = d.pop("location", UNSET)

        url = d.pop("url", UNSET)

        avatar_url = d.pop("avatar_url", UNSET)

        banner_url = d.pop("banner_url", UNSET)

        verified = d.pop("verified", UNSET)

        protected = d.pop("protected", UNSET)

        likes = d.pop("likes", UNSET)

        listed = d.pop("listed", UNSET)

        pinned_tweet_ids = cast(list[str], d.pop("pinned_tweet_ids", UNSET))

        user = cls(
            id=id,
            handle=handle,
            name=name,
            followers=followers,
            following=following,
            tweets=tweets,
            created_at=created_at,
            bio=bio,
            location=location,
            url=url,
            avatar_url=avatar_url,
            banner_url=banner_url,
            verified=verified,
            protected=protected,
            likes=likes,
            listed=listed,
            pinned_tweet_ids=pinned_tweet_ids,
        )

        user.additional_properties = d
        return user

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
