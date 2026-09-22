from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListPacksResponse200RateLimitsItem")


@_attrs_define
class ListPacksResponse200RateLimitsItem:
    """
    Attributes:
        paid_usd (int | Unset):  Example: 10.
        requests_per_second (int | Unset):  Example: 20.
    """

    paid_usd: int | Unset = UNSET
    requests_per_second: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        paid_usd = self.paid_usd

        requests_per_second = self.requests_per_second

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if paid_usd is not UNSET:
            field_dict["paid_usd"] = paid_usd
        if requests_per_second is not UNSET:
            field_dict["requests_per_second"] = requests_per_second

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        paid_usd = d.pop("paid_usd", UNSET)

        requests_per_second = d.pop("requests_per_second", UNSET)

        list_packs_response_200_rate_limits_item = cls(
            paid_usd=paid_usd,
            requests_per_second=requests_per_second,
        )

        list_packs_response_200_rate_limits_item.additional_properties = d
        return list_packs_response_200_rate_limits_item

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
