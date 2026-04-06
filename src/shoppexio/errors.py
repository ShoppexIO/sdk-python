from __future__ import annotations


class ShoppexApiError(Exception):
    def __init__(
        self,
        message: str,
        status: int,
        request_id: str | None = None,
        code: str | None = None,
        doc_url: str | None = None,
        details=None,
        raw=None,
    ):
        super().__init__(message)
        self.status = status
        self.request_id = request_id
        self.code = code
        self.doc_url = doc_url
        self.details = details
        self.raw = raw
