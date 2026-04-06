from __future__ import annotations

from typing import Any, Iterator

import httpx

from .errors import ShoppexApiError
from .models import (
    CouponResource,
    CustomerResource,
    InvoiceResource,
    OrderResource,
    PaymentResource,
    ProductResource,
    ShoppexResource,
    ShoppexResponse,
    WebhookResource,
    parse_resource,
    parse_response,
)


class _BaseService:
    def __init__(self, client: "ShoppexClient"):
        self._client = client


class MeService(_BaseService):
    def get(self) -> ShoppexResponse[Any]:
        return self._client.response("GET", "/dev/v1/me")

    def capabilities(self) -> ShoppexResponse[Any]:
        return self._client.response("GET", "/dev/v1/me/capabilities")


class ProductsService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[ProductResource]]:
        return self._client.response("GET", "/dev/v1/products/", params=query, resource_type=ProductResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[ProductResource]:
        return self._client.collect_cursor("/dev/v1/products/", query, resource_type=ProductResource)

    def get(self, product_id: str) -> ShoppexResponse[ProductResource]:
        return self._client.response("GET", f"/dev/v1/products/{product_id}", resource_type=ProductResource)

    def create(self, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[ProductResource]:
        return self._client.response("POST", "/dev/v1/products/", json=payload, idempotency_key=idempotency_key, resource_type=ProductResource)

    def update(self, product_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[ProductResource]:
        return self._client.response("PATCH", f"/dev/v1/products/{product_id}", json=payload, idempotency_key=idempotency_key, resource_type=ProductResource)

    def delete(self, product_id: str, idempotency_key: str | None = None) -> ShoppexResponse[Any]:
        return self._client.response("DELETE", f"/dev/v1/products/{product_id}", idempotency_key=idempotency_key)


class OrdersService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[OrderResource]]:
        return self._client.response("GET", "/dev/v1/orders", params=query, resource_type=OrderResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[OrderResource]:
        return self._client.collect_cursor("/dev/v1/orders", query, resource_type=OrderResource)

    def get(self, order_id: str) -> ShoppexResponse[OrderResource]:
        return self._client.response("GET", f"/dev/v1/orders/{order_id}", resource_type=OrderResource)

    def create(self, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[OrderResource]:
        return self._client.response("POST", "/dev/v1/orders", json=payload, idempotency_key=idempotency_key, resource_type=OrderResource)

    def update(self, order_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[OrderResource]:
        return self._client.response("PATCH", f"/dev/v1/orders/{order_id}", json=payload, idempotency_key=idempotency_key, resource_type=OrderResource)

    def fulfill(self, order_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[OrderResource]:
        return self._client.response("POST", f"/dev/v1/orders/{order_id}/fulfill", json=payload, idempotency_key=idempotency_key, resource_type=OrderResource)

    def complete(self, order_id: str, payload: dict[str, Any] | None = None, idempotency_key: str | None = None) -> ShoppexResponse[OrderResource]:
        return self._client.response(
            "POST",
            f"/dev/v1/orders/{order_id}/complete",
            json=payload or {},
            idempotency_key=idempotency_key,
            resource_type=OrderResource,
        )

    def refund(self, order_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[OrderResource]:
        return self._client.response("POST", f"/dev/v1/orders/{order_id}/refund", json=payload, idempotency_key=idempotency_key, resource_type=OrderResource)


class CustomersService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[CustomerResource]]:
        return self._client.response("GET", "/dev/v1/customers", params=query, resource_type=CustomerResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[CustomerResource]:
        return self._client.collect_cursor("/dev/v1/customers", query, resource_type=CustomerResource)

    def get(self, customer_id: str) -> ShoppexResponse[CustomerResource]:
        return self._client.response("GET", f"/dev/v1/customers/{customer_id}", resource_type=CustomerResource)

    def create(self, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[CustomerResource]:
        return self._client.response("POST", "/dev/v1/customers", json=payload, idempotency_key=idempotency_key, resource_type=CustomerResource)

    def update(self, customer_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[CustomerResource]:
        return self._client.response("PATCH", f"/dev/v1/customers/{customer_id}", json=payload, idempotency_key=idempotency_key, resource_type=CustomerResource)

    def delete(self, customer_id: str, idempotency_key: str | None = None) -> ShoppexResponse[Any]:
        return self._client.response("DELETE", f"/dev/v1/customers/{customer_id}", idempotency_key=idempotency_key)


class PaymentsService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[PaymentResource]]:
        return self._client.response("GET", "/dev/v1/payments", params=query, resource_type=PaymentResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[PaymentResource]:
        return self._client.collect_cursor("/dev/v1/payments", query, resource_type=PaymentResource)

    def get(self, uniqid: str) -> ShoppexResponse[PaymentResource]:
        return self._client.response("GET", f"/dev/v1/payments/{uniqid}", resource_type=PaymentResource)

    def create(self, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[PaymentResource]:
        return self._client.response("POST", "/dev/v1/payments", json=payload, idempotency_key=idempotency_key, resource_type=PaymentResource)

    def complete(self, uniqid: str, payload: dict[str, Any] | None = None, idempotency_key: str | None = None) -> ShoppexResponse[PaymentResource]:
        return self._client.response(
            "POST",
            f"/dev/v1/payments/{uniqid}/complete",
            json=payload or {},
            idempotency_key=idempotency_key,
            resource_type=PaymentResource,
        )


class InvoicesService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[InvoiceResource]]:
        return self._client.response("GET", "/dev/v1/invoices", params=query, resource_type=InvoiceResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[InvoiceResource]:
        return self._client.collect_cursor("/dev/v1/invoices", query, resource_type=InvoiceResource)

    def get(self, uniqid: str) -> ShoppexResponse[InvoiceResource]:
        return self._client.response("GET", f"/dev/v1/invoices/{uniqid}", resource_type=InvoiceResource)

    def complete(self, uniqid: str, payload: dict[str, Any] | None = None, idempotency_key: str | None = None) -> ShoppexResponse[InvoiceResource]:
        return self._client.response(
            "POST",
            f"/dev/v1/invoices/{uniqid}/complete",
            json=payload or {},
            idempotency_key=idempotency_key,
            resource_type=InvoiceResource,
        )


class CouponsService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[CouponResource]]:
        return self._client.response("GET", "/dev/v1/coupons/", params=query, resource_type=CouponResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[CouponResource]:
        return self._client.collect_cursor("/dev/v1/coupons/", query, resource_type=CouponResource)

    def get(self, coupon_id: str) -> ShoppexResponse[CouponResource]:
        return self._client.response("GET", f"/dev/v1/coupons/{coupon_id}", resource_type=CouponResource)

    def get_by_code(self, code: str) -> ShoppexResponse[CouponResource]:
        return self._client.response("GET", f"/dev/v1/coupons/code/{code}", resource_type=CouponResource)

    def create(self, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[CouponResource]:
        return self._client.response("POST", "/dev/v1/coupons/", json=payload, idempotency_key=idempotency_key, resource_type=CouponResource)

    def update(self, coupon_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[CouponResource]:
        return self._client.response("PATCH", f"/dev/v1/coupons/{coupon_id}", json=payload, idempotency_key=idempotency_key, resource_type=CouponResource)

    def delete(self, coupon_id: str, idempotency_key: str | None = None) -> ShoppexResponse[Any]:
        return self._client.response("DELETE", f"/dev/v1/coupons/{coupon_id}", idempotency_key=idempotency_key)


class WebhooksService(_BaseService):
    def list(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[WebhookResource]]:
        return self._client.response("GET", "/dev/v1/webhooks", params=query, resource_type=WebhookResource)

    def list_all(self, query: dict[str, Any] | None = None) -> list[WebhookResource]:
        return self._client.collect_cursor("/dev/v1/webhooks", query, resource_type=WebhookResource)

    def get(self, webhook_id: str) -> ShoppexResponse[WebhookResource]:
        return self._client.response("GET", f"/dev/v1/webhooks/{webhook_id}", resource_type=WebhookResource)

    def create(self, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[WebhookResource]:
        return self._client.response("POST", "/dev/v1/webhooks", json=payload, idempotency_key=idempotency_key, resource_type=WebhookResource)

    def update(self, webhook_id: str, payload: dict[str, Any], idempotency_key: str | None = None) -> ShoppexResponse[WebhookResource]:
        return self._client.response("PATCH", f"/dev/v1/webhooks/{webhook_id}", json=payload, idempotency_key=idempotency_key, resource_type=WebhookResource)

    def delete(self, webhook_id: str, idempotency_key: str | None = None) -> ShoppexResponse[Any]:
        return self._client.response("DELETE", f"/dev/v1/webhooks/{webhook_id}", idempotency_key=idempotency_key)

    def events(self) -> ShoppexResponse[Any]:
        return self._client.response("GET", "/dev/v1/webhooks/events")

    def logs(self, query: dict[str, Any] | None = None) -> ShoppexResponse[list[ShoppexResource]]:
        return self._client.response("GET", "/dev/v1/webhooks/logs", params=query)

    def logs_all(self, query: dict[str, Any] | None = None) -> list[ShoppexResource]:
        return self._client.collect_page("/dev/v1/webhooks/logs", query)

    def test(self, webhook_id: str, payload: dict[str, Any] | None = None, idempotency_key: str | None = None) -> ShoppexResponse[WebhookResource]:
        return self._client.response(
            "POST",
            f"/dev/v1/webhooks/{webhook_id}/test",
            json=payload or {},
            idempotency_key=idempotency_key,
            resource_type=WebhookResource,
        )

    def rotate_secret(self, webhook_id: str, payload: dict[str, Any] | None = None, idempotency_key: str | None = None) -> ShoppexResponse[WebhookResource]:
        return self._client.response(
            "POST",
            f"/dev/v1/webhooks/{webhook_id}/rotate-secret",
            json=payload or {},
            idempotency_key=idempotency_key,
            resource_type=WebhookResource,
        )

    def retry_log(self, log_id: str, payload: dict[str, Any] | None = None, idempotency_key: str | None = None) -> ShoppexResponse[Any]:
        return self._client.response(
            "POST",
            f"/dev/v1/webhooks/logs/{log_id}/retry",
            json=payload or {},
            idempotency_key=idempotency_key,
        )


class ShoppexClient:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        access_token: str | None = None,
        base_url: str = "https://api.shoppex.io",
        timeout: float = 30.0,
        http_client: Any | None = None,
    ):
        token = api_key or access_token
        if not token:
            raise ValueError("ShoppexClient requires either api_key or access_token.")

        self.base_url = base_url.rstrip("/")
        self._http = http_client or httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
        )

        self.me = MeService(self)
        self.products = ProductsService(self)
        self.orders = OrdersService(self)
        self.customers = CustomersService(self)
        self.payments = PaymentsService(self)
        self.invoices = InvoicesService(self)
        self.coupons = CouponsService(self)
        self.webhooks = WebhooksService(self)

    def response(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        resource_type: type[ShoppexResource] = ShoppexResource,
    ) -> ShoppexResponse[Any]:
        return parse_response(
            self.request(
                method,
                path,
                params=params,
                json=json,
                idempotency_key=idempotency_key,
            ),
            resource_type,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        headers: dict[str, str] = {}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        response = self._http.request(method, path, params=params, json=json, headers=headers)

        try:
            payload = response.json()
        except ValueError:
            payload = None

        if response.is_error:
            message = "Shoppex API request failed."
            code = None
            doc_url = None
            details = payload

            if isinstance(payload, dict):
                nested = payload.get("error")
                if isinstance(nested, dict):
                    if isinstance(nested.get("message"), str):
                        message = nested["message"]
                    code = nested.get("code") if isinstance(nested.get("code"), str) else None
                    doc_url = nested.get("doc_url") if isinstance(nested.get("doc_url"), str) else None
                    details = nested.get("details")
                elif isinstance(payload.get("message"), str):
                    message = payload["message"]

            raise ShoppexApiError(
                message,
                status=response.status_code,
                request_id=response.headers.get("x-request-id"),
                code=code,
                doc_url=doc_url,
                details=details,
                raw=payload,
            )

        return payload if isinstance(payload, dict) else {"data": payload}

    def iterate_cursor(
        self,
        path: str,
        query: dict[str, Any] | None = None,
        resource_type: type[ShoppexResource] = ShoppexResource,
    ) -> Iterator[ShoppexResource]:
        cursor = query.get("cursor") if query else None

        while True:
            params = dict(query or {})
            if cursor:
                params["cursor"] = cursor

            response = self.request("GET", path, params=params)

            for item in response.get("data", []):
                parsed_item = parse_resource(item, resource_type)
                if isinstance(parsed_item, ShoppexResource):
                    yield parsed_item

            pagination = response.get("pagination", {})
            has_more = bool(pagination.get("has_more"))
            cursor = pagination.get("next_cursor")

            if not has_more or not cursor:
                break

    def collect_cursor(
        self,
        path: str,
        query: dict[str, Any] | None = None,
        resource_type: type[ShoppexResource] = ShoppexResource,
    ) -> list[ShoppexResource]:
        return list(self.iterate_cursor(path, query, resource_type))

    def collect_page(
        self,
        path: str,
        query: dict[str, Any] | None = None,
        resource_type: type[ShoppexResource] = ShoppexResource,
    ) -> list[ShoppexResource]:
        items: list[ShoppexResource] = []
        page = int((query or {}).get("page", 1))

        while True:
            params = dict(query or {})
            params["page"] = page
            response = self.request("GET", path, params=params)
            for item in response.get("data", []):
                parsed_item = parse_resource(item, resource_type)
                if isinstance(parsed_item, ShoppexResource):
                    items.append(parsed_item)

            pagination = response.get("pagination", {})
            if not pagination.get("has_more"):
                break

            page += 1

        return items
