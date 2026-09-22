from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.error_body import ErrorBody


T = TypeVar("T", bound="Error")


@_attrs_define
class Error:
    """Every failure from this API, in one shape. Charged nothing, always carries a
    `request_id`. The same failure is available as RFC 9457 `application/problem+json`
    to callers that ask for it.

        Attributes:
            error (ErrorBody): The failure itself. `code` is stable; match on it, never on `message`.
            request_id (str):
    """

    error: ErrorBody
    request_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error = self.error.to_dict()

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error": error,
                "request_id": request_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_body import ErrorBody  # noqa: PLC0415

        d = dict(src_dict)
        error = ErrorBody.from_dict(d.pop("error"))

        request_id = d.pop("request_id")

        error = cls(
            error=error,
            request_id=request_id,
        )

        error.additional_properties = d
        return error

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
