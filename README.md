# shoppexio

Official Python SDK for the Shoppex Developer API.

## Install

```bash
pip install shoppexio
```

## Quick Start

```python
from shoppexio import ShoppexClient

client = ShoppexClient(api_key="shx_your_api_key")

me = client.me.get()
products = client.products.list({"page": 1, "limit": 20})
```

## Auth

Use one of these:

- `api_key` for your own server-to-server integrations
- `access_token` for OAuth app installs

## Status

This SDK is in early public MVP stage.
The package shape is in place, and the main next step is broadening endpoint coverage and polishing the response types.

## Docs

- Developer API docs: [docs.shoppex.io/api-reference/introduction](https://docs.shoppex.io/api-reference/introduction)
- SDK docs: [docs.shoppex.io/api-reference/sdks](https://docs.shoppex.io/api-reference/sdks)
