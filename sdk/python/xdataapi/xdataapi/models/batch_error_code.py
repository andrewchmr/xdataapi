from enum import StrEnum


class BatchErrorCode(StrEnum):
    ACCESS_DENIED = "access_denied"
    BAD_REQUEST = "bad_request"
    NOT_FOUND = "not_found"
    NO_ACCOUNT = "no_account"
    NO_CREDITS = "no_credits"
    REQUEST_REJECTED = "request_rejected"
    UPSTREAM_ERROR = "upstream_error"
    UPSTREAM_RATE_LIMITED = "upstream_rate_limited"

    def __str__(self) -> str:
        return str(self.value)
