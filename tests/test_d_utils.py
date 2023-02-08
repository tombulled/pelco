import pytest

from pelcod.errors import ValidationError
from pelcod.utils import calculate_checksum, sep_uint16


def test_calculate_checksum() -> None:
    assert calculate_checksum(()) == 0
    assert calculate_checksum((1, 2, 3)) == 6
    assert calculate_checksum((64, 128, 255)) == 191

    with pytest.raises(ValidationError):
        calculate_checksum((1, 2, 3, 256))

    with pytest.raises(ValidationError):
        calculate_checksum((1, 2, 3, -1))


def test_sep_uint16() -> None:
    assert sep_uint16(0xABCD) == (0xAB, 0xCD)
    assert sep_uint16(0xDEAD) == (0xDE, 0xAD)

    with pytest.raises(ValidationError):
        sep_uint16(0xFFFF + 1)

    with pytest.raises(ValidationError):
        sep_uint16(-1)
