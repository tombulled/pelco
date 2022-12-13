from typing import Sequence

from .constants import BYTE_MAX, BYTE_MIN


def calculate_checksum(bytes: Sequence[int], /) -> int:
    checksum: int = 0x00

    byte: int
    for byte in bytes:
        assert BYTE_MIN <= byte <= BYTE_MAX

        checksum += byte

    return checksum % (BYTE_MAX + 1)
