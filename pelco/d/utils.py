from typing import Sequence, Tuple

from .constants import UINT8_MAX, UINT8_SIZE
from .typing import UInt8, UInt16
from .validators import validate_uint8, validate_uint16


def calculate_checksum(values: Sequence[UInt8], /) -> UInt8:
    checksum: UInt8 = 0x00

    value: UInt8
    for value in values:
        validate_uint8(value)

        checksum += value

    return checksum % (UINT8_MAX + 1)


def sep_uint16(data: UInt16, /) -> Tuple[UInt8, UInt8]:
    validate_uint16(data)

    data_1: UInt8 = (data >> UINT8_SIZE) & UINT8_MAX
    data_2: UInt8 = data & UINT8_MAX

    return (data_1, data_2)
