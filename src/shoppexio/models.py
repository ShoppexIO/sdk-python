from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R", bound="ShoppexResource")


@dataclass
class ShoppexResource:
    raw: dict[str, Any]

    @property
    def id(self) -> str | None:
        value = self.raw.get("id")
        return value if isinstance(value, str) else None

    @property
    def uniqid(self) -> str | None:
        value = self.raw.get("uniqid")
        return value if isinstance(value, str) else None

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.raw)

    def __getitem__(self, key: str) -> Any:
        return self.raw[key]

    def __contains__(self, key: object) -> bool:
        return key in self.raw


@dataclass
class ProductResource(ShoppexResource):
    @property
    def name(self) -> str | None:
        value = self.raw.get("name")
        return value if isinstance(value, str) else None


@dataclass
class OrderResource(ShoppexResource):
    @property
    def status(self) -> str | None:
        value = self.raw.get("status")
        return value if isinstance(value, str) else None


@dataclass
class CustomerResource(ShoppexResource):
    @property
    def email(self) -> str | None:
        value = self.raw.get("email")
        return value if isinstance(value, str) else None


@dataclass
class PaymentResource(ShoppexResource):
    @property
    def status(self) -> str | None:
        value = self.raw.get("status")
        return value if isinstance(value, str) else None


@dataclass
class InvoiceResource(ShoppexResource):
    @property
    def status(self) -> str | None:
        value = self.raw.get("status")
        return value if isinstance(value, str) else None


@dataclass
class CouponResource(ShoppexResource):
    @property
    def code(self) -> str | None:
        value = self.raw.get("code")
        return value if isinstance(value, str) else None


@dataclass
class WebhookResource(ShoppexResource):
    @property
    def url(self) -> str | None:
        value = self.raw.get("url")
        return value if isinstance(value, str) else None


@dataclass
class CursorPagination:
    has_more: bool = False
    next_cursor: str | None = None


@dataclass
class PagePagination:
    page: int | None = None
    limit: int | None = None
    total: int | None = None
    total_pages: int | None = None
    has_more: bool = False


@dataclass
class ShoppexResponse(Generic[T]):
    data: T
    pagination: CursorPagination | PagePagination | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.raw)


def parse_resource(value: Any, resource_type: type[R] = ShoppexResource) -> Any:
    if isinstance(value, dict):
        return resource_type(value)

    return value


def parse_pagination(value: Any) -> CursorPagination | PagePagination | None:
    if not isinstance(value, dict):
        return None

    if "next_cursor" in value:
        next_cursor = value.get("next_cursor")
        return CursorPagination(
            has_more=bool(value.get("has_more")),
            next_cursor=next_cursor if isinstance(next_cursor, str) else None,
        )

    return PagePagination(
        page=value.get("page") if isinstance(value.get("page"), int) else None,
        limit=value.get("limit") if isinstance(value.get("limit"), int) else None,
        total=value.get("total") if isinstance(value.get("total"), int) else None,
        total_pages=value.get("total_pages") if isinstance(value.get("total_pages"), int) else None,
        has_more=bool(value.get("has_more")),
    )


def parse_response(payload: dict[str, Any], resource_type: type[R] = ShoppexResource) -> ShoppexResponse[Any]:
    data = payload.get("data")

    if isinstance(data, list):
        parsed_data = [parse_resource(item, resource_type) for item in data]
    else:
        parsed_data = parse_resource(data, resource_type)

    return ShoppexResponse(
        data=parsed_data,
        pagination=parse_pagination(payload.get("pagination")),
        raw=payload,
    )
