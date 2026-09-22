from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.error_body import ErrorBody


T = TypeVar("T", bound="Problem")


@_attrs_define
class Problem:
    """RFC 9457 view of the same failure, served when the caller sends
    `Accept: application/problem+json`. Nothing new is reported — `type`, `title`,
    `status` and `detail` are the registered names for what `error.code` and
    `error.message` already said, so a generic client can read a failure it has no
    specific handling for.

        Attributes:
            type_ (str): A page describing this error code. Example: https://xdataapi.io/docs/errors#no_credits.
            title (str):  Example: Balance is zero.
            status (int):  Example: 402.
            code (str): The same value as `error.code`. Stable; match on this, not on the text.
            request_id (str):
            detail (str | Unset): The same text as `error.message`.
            error (ErrorBody | Unset): The failure itself. `code` is stable; match on it, never on `message`.
    """

    type_: str
    title: str
    status: int
    code: str
    request_id: str
    detail: str | Unset = UNSET
    error: ErrorBody | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        title = self.title

        status = self.status

        code = self.code

        request_id = self.request_id

        detail = self.detail

        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "title": title,
                "status": status,
                "code": code,
                "request_id": request_id,
            }
        )
        if detail is not UNSET:
            field_dict["detail"] = detail
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.error_body import ErrorBody  # noqa: PLC0415

        d = dict(src_dict)
        type_ = d.pop("type")

        title = d.pop("title")

        status = d.pop("status")

        code = d.pop("code")

        request_id = d.pop("request_id")

        detail = d.pop("detail", UNSET)

        _error = d.pop("error", UNSET)
        error: ErrorBody | Unset
        if isinstance(_error, Unset):
            error = UNSET
        else:
            error = ErrorBody.from_dict(_error)

        problem = cls(
            type_=type_,
            title=title,
            status=status,
            code=code,
            request_id=request_id,
            detail=detail,
            error=error,
        )

        problem.additional_properties = d
        return problem

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
