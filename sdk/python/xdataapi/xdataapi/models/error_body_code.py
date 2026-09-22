from enum import StrEnum


class ErrorBodyCode(StrEnum):
    ACCESS_DENIED = "access_denied"
    BAD_REQUEST = "bad_request"
    BILLING_DISABLED = "billing_disabled"
    INTERNAL = "internal"
    INVALID_KEY = "invalid_key"
    MISSING_KEY = "missing_key"
    NOT_FOUND = "not_found"
    NO_ACCOUNT = "no_account"
    NO_CREDITS = "no_credits"
    PRODUCT_UNAVAILABLE = "product_unavailable"
    QUERY_ID_STALE = "query_id_stale"
    RATE_LIMITED = "rate_limited"
    REQUEST_REJECTED = "request_rejected"
    UPSTREAM_ERROR = "upstream_error"
    UPSTREAM_RATE_LIMITED = "upstream_rate_limited"

    def __str__(self) -> str:
        return str(self.value)
