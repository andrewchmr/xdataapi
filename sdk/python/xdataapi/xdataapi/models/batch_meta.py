from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.batch_meta_cache import BatchMetaCache

if TYPE_CHECKING:
    from ..models.batch_error import BatchError


T = TypeVar("T", bound="BatchMeta")


@_attrs_define
class BatchMeta:
    """
    Attributes:
        errors (list[BatchError]): Inputs that returned nothing, with the reason. Never charged.
        items (int): Objects returned.
        credits_charged (float):
        balance_remaining (float):
        cache (BatchMetaCache):
        cache_hits (int): Objects served from cache
        request_id (UUID):
    """

    errors: list[BatchError]
    items: int
    credits_charged: float
    balance_remaining: float
    cache: BatchMetaCache
    cache_hits: int
    request_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        errors = []
        for errors_item_data in self.errors:
            errors_item = errors_item_data.to_dict()
            errors.append(errors_item)

        items = self.items

        credits_charged = self.credits_charged

        balance_remaining = self.balance_remaining

        cache = self.cache.value

        cache_hits = self.cache_hits

        request_id = str(self.request_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errors": errors,
                "items": items,
                "credits_charged": credits_charged,
                "balance_remaining": balance_remaining,
                "cache": cache,
                "cache_hits": cache_hits,
                "request_id": request_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.batch_error import BatchError  # noqa: PLC0415

        d = dict(src_dict)
        errors = []
        _errors = d.pop("errors")
        for errors_item_data in _errors:
            errors_item = BatchError.from_dict(errors_item_data)

            errors.append(errors_item)

        items = d.pop("items")

        credits_charged = d.pop("credits_charged")

        balance_remaining = d.pop("balance_remaining")

        cache = BatchMetaCache(d.pop("cache"))

        cache_hits = d.pop("cache_hits")

        request_id = UUID(d.pop("request_id"))

        batch_meta = cls(
            errors=errors,
            items=items,
            credits_charged=credits_charged,
            balance_remaining=balance_remaining,
            cache=cache,
            cache_hits=cache_hits,
            request_id=request_id,
        )

        batch_meta.additional_properties = d
        return batch_meta

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
