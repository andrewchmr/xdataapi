from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListPacksResponse200DataItem")


@_attrs_define
class ListPacksResponse200DataItem:
    """
    Attributes:
        name (str | Unset):  Example: starter.
        usd (int | Unset):  Example: 10.
        credits_ (int | Unset):  Example: 80000.
        buyable (bool | Unset):
    """

    name: str | Unset = UNSET
    usd: int | Unset = UNSET
    credits_: int | Unset = UNSET
    buyable: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        usd = self.usd

        credits_ = self.credits_

        buyable = self.buyable

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if usd is not UNSET:
            field_dict["usd"] = usd
        if credits_ is not UNSET:
            field_dict["credits"] = credits_
        if buyable is not UNSET:
            field_dict["buyable"] = buyable

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        usd = d.pop("usd", UNSET)

        credits_ = d.pop("credits", UNSET)

        buyable = d.pop("buyable", UNSET)

        list_packs_response_200_data_item = cls(
            name=name,
            usd=usd,
            credits_=credits_,
            buyable=buyable,
        )

        list_packs_response_200_data_item.additional_properties = d
        return list_packs_response_200_data_item

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
