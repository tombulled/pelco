from dataclasses import dataclass
from typing import Generic, TypeVar

from .enums import EventType

T = TypeVar("T")


@dataclass
class Event(Generic[T]):
    type: EventType
    subject: T
    value: int