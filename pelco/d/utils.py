from typing import Sequence

from .constants import UINT8_MAX, UINT8_MIN


def calculate_checksum(bytes: Sequence[int], /) -> int:
    checksum: int = 0x00

    byte: int
    for byte in bytes:
        assert UINT8_MIN <= byte <= UINT8_MAX

        checksum += byte

    return checksum % (UINT8_MAX + 1)
