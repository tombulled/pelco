import pytest

from pelcod.errors import ValidationError
from pelcod.validators import validate_even, validate_odd


def test_validate_odd() -> None:
    validate_odd(1)

    with pytest.raises(ValidationError):
        validate_odd(2)


def test_validate_even() -> None:
    validate_even(2)

    with pytest.raises(ValidationError):
        validate_even(1)
