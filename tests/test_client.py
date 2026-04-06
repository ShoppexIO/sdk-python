from __future__ import annotations

import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))

from shoppexio import (
    CouponResource,
    CursorPagination,
    InvoiceResource,
    PagePagination,
    PaymentResource,
    ProductResource,
    ShoppexApiError,
    ShoppexClient,
    ShoppexResource,
    WebhookResource,
)  # noqa: E402


class FakeResponse:
    def __init__(self, payload, status_code=200, headers=None):
        self._payload = payload
        self.status_code = status_code
        self.headers = headers or {}
        self.is_error = status_code >= 400

    def json(self):
        return self._payload


class FakeHttpClient:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, path, params=None, json=None, headers=None):
        self.calls.append({
            "method": method,
            "path": path,
            "params": params,
            "json": json,
            "headers": headers,
        })
        return self.responses.pop(0)


class ShoppexClientTests(unittest.TestCase):
    def test_collect_cursor_pages(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "data": [{"id": "prod_1"}, {"id": "prod_2"}],
                "pagination": {"next_cursor": "cursor_2", "has_more": True},
            }),
            FakeResponse({
                "data": [{"id": "prod_3"}],
                "pagination": {"next_cursor": None, "has_more": False},
            }),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        result = client.products.list_all({"limit": 2})

        self.assertEqual([item.id for item in result], ["prod_1", "prod_2", "prod_3"])
        self.assertEqual(len(fake_http.calls), 2)
        self.assertEqual(fake_http.calls[1]["params"]["cursor"], "cursor_2")

    def test_collect_page_lists(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "data": [{"id": "log_1"}],
                "pagination": {"page": 1, "limit": 1, "total": 2, "total_pages": 2, "has_more": True},
            }),
            FakeResponse({
                "data": [{"id": "log_2"}],
                "pagination": {"page": 2, "limit": 1, "total": 2, "total_pages": 2, "has_more": False},
            }),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        result = client.webhooks.logs_all({"page": 1, "limit": 1})

        self.assertEqual([item.id for item in result], ["log_1", "log_2"])
        self.assertEqual(fake_http.calls[1]["params"]["page"], 2)

    def test_returns_typed_response_models(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "data": [{"id": "prod_1", "name": "Starter"}],
                "pagination": {"next_cursor": "cursor_2", "has_more": True},
            }),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        result = client.products.list({"limit": 1})

        self.assertIsInstance(result.pagination, CursorPagination)
        self.assertEqual(result.pagination.next_cursor, "cursor_2")
        self.assertEqual(result.data[0].name, "Starter")
        self.assertIsInstance(result.data[0], ProductResource)

    def test_returns_typed_secondary_resources(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "data": [{"uniqid": "pay_1", "status": "pending"}],
                "pagination": {"next_cursor": None, "has_more": False},
            }),
            FakeResponse({
                "data": {"uniqid": "inv_1", "status": "open"},
            }),
            FakeResponse({
                "data": {"id": "coupon_1", "code": "SPRING25"},
            }),
            FakeResponse({
                "data": {"id": "wh_1", "url": "https://example.com/webhook"},
            }),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        payments = client.payments.list({"limit": 1})
        invoice = client.invoices.get("inv_1")
        coupon = client.coupons.get("coupon_1")
        webhook = client.webhooks.get("wh_1")

        self.assertIsInstance(payments.data[0], PaymentResource)
        self.assertEqual(payments.data[0].status, "pending")
        self.assertIsInstance(invoice.data, InvoiceResource)
        self.assertEqual(invoice.data.status, "open")
        self.assertIsInstance(coupon.data, CouponResource)
        self.assertEqual(coupon.data.code, "SPRING25")
        self.assertIsInstance(webhook.data, WebhookResource)
        self.assertEqual(webhook.data.url, "https://example.com/webhook")

    def test_mutation_helpers_forward_idempotency_key(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "data": {"id": "ord_1", "status": "completed"},
            }),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        result = client.orders.complete(
            "ord_1",
            {"notify_customer": True},
            idempotency_key="idem_123",
        )

        self.assertEqual(result.data.get("status"), "completed")
        self.assertEqual(fake_http.calls[0]["headers"]["Idempotency-Key"], "idem_123")

    def test_parses_structured_error(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Missing or invalid API key.",
                    "doc_url": "https://docs.shoppex.io/api/errors#UNAUTHORIZED",
                    "details": [{"field": "authorization", "message": "Missing bearer token"}],
                }
            }, status_code=401, headers={"x-request-id": "req_123"}),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        with self.assertRaises(ShoppexApiError) as ctx:
            client.me.get()

        error = ctx.exception
        self.assertEqual(error.status, 401)
        self.assertEqual(error.code, "UNAUTHORIZED")
        self.assertEqual(error.doc_url, "https://docs.shoppex.io/api/errors#UNAUTHORIZED")
        self.assertEqual(error.request_id, "req_123")

    def test_page_based_response_uses_page_pagination_model(self):
        fake_http = FakeHttpClient([
            FakeResponse({
                "data": [{"id": "log_1"}],
                "pagination": {"page": 1, "limit": 1, "total": 1, "total_pages": 1, "has_more": False},
            }),
        ])
        client = ShoppexClient(api_key="shx_test", http_client=fake_http)

        result = client.webhooks.logs({"page": 1, "limit": 1})

        self.assertIsInstance(result.pagination, PagePagination)
        self.assertEqual(result.pagination.page, 1)


if __name__ == "__main__":
    unittest.main()
