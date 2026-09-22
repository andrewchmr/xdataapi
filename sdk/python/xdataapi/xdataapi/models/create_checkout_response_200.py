from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCheckoutResponse200")


@_attrs_define
class CreateCheckoutResponse200:
    """
    Attributes:
        url (str | Unset):
        pack (str | Unset):
        usd (int | Unset):
        credits_ (int | Unset):
        request_id (str | Unset):
    """

    url: str | Unset = UNSET
    pack: str | Unset = UNSET
    usd: int | Unset = UNSET
    credits_: int | Unset = UNSET
    request_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        pack = self.pack

        usd = self.usd

        credits_ = self.credits_

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if pack is not UNSET:
            field_dict["pack"] = pack
        if usd is not UNSET:
            field_dict["usd"] = usd
        if credits_ is not UNSET:
            field_dict["credits"] = credits_
        if request_id is not UNSET:
            field_dict["request_id"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        pack = d.pop("pack", UNSET)

        usd = d.pop("usd", UNSET)

        credits_ = d.pop("credits", UNSET)

        request_id = d.pop("request_id", UNSET)

        create_checkout_response_200 = cls(
            url=url,
            pack=pack,
            usd=usd,
            credits_=credits_,
            request_id=request_id,
        )

        create_checkout_response_200.additional_properties = d
        return create_checkout_response_200

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
