import pytest

from pelco.d.errors import ValidationError
from pelco.d.validators import validate_odd, validate_even


def test_validate_odd() -> None:
    validate_odd(1)

    with pytest.raises(ValidationError):
        validate_odd(2)


def test_validate_even() -> None:
    validate_even(2)

    with pytest.raises(ValidationError):
        validate_even(1)
