from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_packs_response_200_data_item import ListPacksResponse200DataItem
    from ..models.list_packs_response_200_rate_limits_item import ListPacksResponse200RateLimitsItem


T = TypeVar("T", bound="ListPacksResponse200")


@_attrs_define
class ListPacksResponse200:
    """
    Attributes:
        data (list[ListPacksResponse200DataItem] | Unset):
        rate_limits (list[ListPacksResponse200RateLimitsItem] | Unset): Requests per second by the total paid over the
            account's life. The limit only goes up.
    """

    data: list[ListPacksResponse200DataItem] | Unset = UNSET
    rate_limits: list[ListPacksResponse200RateLimitsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.to_dict()
                data.append(data_item)

        rate_limits: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.rate_limits, Unset):
            rate_limits = []
            for rate_limits_item_data in self.rate_limits:
                rate_limits_item = rate_limits_item_data.to_dict()
                rate_limits.append(rate_limits_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if rate_limits is not UNSET:
            field_dict["rate_limits"] = rate_limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.list_packs_response_200_data_item import ListPacksResponse200DataItem  # noqa: PLC0415
        from ..models.list_packs_response_200_rate_limits_item import (
            ListPacksResponse200RateLimitsItem,  # noqa: PLC0415
        )

        d = dict(src_dict)
        _data = d.pop("data", UNSET)
        data: list[ListPacksResponse200DataItem] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = ListPacksResponse200DataItem.from_dict(data_item_data)

                data.append(data_item)

        _rate_limits = d.pop("rate_limits", UNSET)
        rate_limits: list[ListPacksResponse200RateLimitsItem] | Unset = UNSET
        if _rate_limits is not UNSET:
            rate_limits = []
            for rate_limits_item_data in _rate_limits:
                rate_limits_item = ListPacksResponse200RateLimitsItem.from_dict(rate_limits_item_data)

                rate_limits.append(rate_limits_item)

        list_packs_response_200 = cls(
            data=data,
            rate_limits=rate_limits,
        )

        list_packs_response_200.additional_properties = d
        return list_packs_response_200

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
