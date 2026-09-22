from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.meta_cache import MetaCache
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user import User


T = TypeVar("T", bound="UserPage")


@_attrs_define
class UserPage:
    """
    Attributes:
        items (int): Objects returned.
        credits_charged (float):  Example: 20.
        balance_remaining (float):  Example: 79980.
        cache (MetaCache):
        request_id (UUID):
        next_cursor (str | Unset):
        data (list[User] | Unset):
    """

    items: int
    credits_charged: float
    balance_remaining: float
    cache: MetaCache
    request_id: UUID
    next_cursor: str | Unset = UNSET
    data: list[User] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        items = self.items

        credits_charged = self.credits_charged

        balance_remaining = self.balance_remaining

        cache = self.cache.value

        request_id = str(self.request_id)

        next_cursor = self.next_cursor

        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "items": items,
                "credits_charged": credits_charged,
                "balance_remaining": balance_remaining,
                "cache": cache,
                "request_id": request_id,
            }
        )
        if next_cursor is not UNSET:
            field_dict["next_cursor"] = next_cursor
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user import User  # noqa: PLC0415

        d = dict(src_dict)
        items = d.pop("items")

        credits_charged = d.pop("credits_charged")

        balance_remaining = d.pop("balance_remaining")

        cache = MetaCache(d.pop("cache"))

        request_id = UUID(d.pop("request_id"))

        next_cursor = d.pop("next_cursor", UNSET)

        _data = d.pop("data", UNSET)
        data: list[User] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = User.from_dict(data_item_data)

                data.append(data_item)

        user_page = cls(
            items=items,
            credits_charged=credits_charged,
            balance_remaining=balance_remaining,
            cache=cache,
            request_id=request_id,
            next_cursor=next_cursor,
            data=data,
        )

        user_page.additional_properties = d
        return user_page

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
