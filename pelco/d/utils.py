from typing import Sequence, Tuple

from .constants import UINT8_MAX, UINT8_SIZE
from .validators import validate_uint8, validate_uint16


def calculate_checksum(bytes: Sequence[int], /) -> int:
    checksum: int = 0x00

    byte: int
    for byte in bytes:
        validate_uint8(byte)

        checksum += byte

    return checksum % (UINT8_MAX + 1)


def sep_uint16(data: int, /) -> Tuple[int, int]:
    validate_uint16(data)

    data_1: int = (data >> UINT8_SIZE) & UINT8_MAX
    data_2: int = data & UINT8_MAX

    return (data_1, data_2)
