from shoppexio import ShoppexApiError, ShoppexClient

client = ShoppexClient(api_key="shx_your_api_key")

me = client.me.get()
print("Connected store:", me.data.get("store_name"))

products = client.products.list({"limit": 20})
for product in products.data:
    print(product.uniqid or product.id, product.name)

try:
    completed = client.orders.complete(
        "ord_123",
        {"notify_customer": True},
        idempotency_key="complete-ord-123",
    )
    print("Order status:", completed.data.status)
except ShoppexApiError as error:
    print(error.status, error.code, error.doc_url)

payments = client.payments.list({"limit": 5})
for payment in payments.data:
    print("Payment:", payment.uniqid, payment.status)
