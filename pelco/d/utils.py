from typing import Sequence, Tuple

from .constants import UINT8_MAX, UINT8_MIN, UINT8_SIZE


def calculate_checksum(bytes: Sequence[int], /) -> int:
    checksum: int = 0x00

    byte: int
    for byte in bytes:
        assert UINT8_MIN <= byte <= UINT8_MAX

        checksum += byte

    return checksum % (UINT8_MAX + 1)


def sep_uint16(data: int) -> Tuple[int, int]:
    data_1: int = (data >> UINT8_SIZE) & UINT8_MAX
    data_2: int = data & UINT8_MAX

    return (data_1, data_2)
