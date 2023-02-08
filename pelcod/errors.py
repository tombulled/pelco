from dataclasses import dataclass
from typing import Sequence

__all__: Sequence[str] = (
    "ChecksumError",
    "RequestError",
    "ResponseError",
    "ValidationError",
)


@dataclass
class ChecksumError(Exception):
    expected: int
    actual: int

    def __str__(self) -> str:
        return f"Expected {self.expected}, got {self.actual}"


class RequestError(Exception):
    pass


class ResponseError(Exception):
    pass


class ValidationError(Exception):
    pass
