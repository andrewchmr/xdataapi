from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetMeResponse200")


@_attrs_define
class GetMeResponse200:
    """
    Attributes:
        customer_id (str | Unset):
        key_prefix (str | Unset):
        balance (float | Unset):
        rate_limit_qps (int | Unset):
    """

    customer_id: str | Unset = UNSET
    key_prefix: str | Unset = UNSET
    balance: float | Unset = UNSET
    rate_limit_qps: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        customer_id = self.customer_id

        key_prefix = self.key_prefix

        balance = self.balance

        rate_limit_qps = self.rate_limit_qps

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if customer_id is not UNSET:
            field_dict["customer_id"] = customer_id
        if key_prefix is not UNSET:
            field_dict["key_prefix"] = key_prefix
        if balance is not UNSET:
            field_dict["balance"] = balance
        if rate_limit_qps is not UNSET:
            field_dict["rate_limit_qps"] = rate_limit_qps

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        customer_id = d.pop("customer_id", UNSET)

        key_prefix = d.pop("key_prefix", UNSET)

        balance = d.pop("balance", UNSET)

        rate_limit_qps = d.pop("rate_limit_qps", UNSET)

        get_me_response_200 = cls(
            customer_id=customer_id,
            key_prefix=key_prefix,
            balance=balance,
            rate_limit_qps=rate_limit_qps,
        )

        get_me_response_200.additional_properties = d
        return get_me_response_200

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
