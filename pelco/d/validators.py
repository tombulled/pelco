from .constants import (
    BYTE_MAX,
    BYTE_MIN,
    MAX_ADDRESS,
    MAX_AUX_ID,
    MAX_FOCUS_SPEED,
    MAX_PAN_SPEED,
    MAX_PATTERN_ID,
    MAX_PRESET_ID,
    MAX_SCREEN_COLUMN,
    MAX_TILT_SPEED,
    MAX_ZONE_ID,
    MAX_ZOOM_SPEED,
    MIN_ADDRESS,
    MIN_AUX_ID,
    MIN_FOCUS_SPEED,
    MIN_PAN_SPEED,
    MIN_PATTERN_ID,
    MIN_PRESET_ID,
    MIN_SCREEN_COLUMN,
    MIN_TILT_SPEED,
    MIN_ZONE_ID,
    MIN_ZOOM_SPEED,
)
from .errors import ValidationError


def validate_in_range(value: int, minimum: int, maximum: int) -> None:
    if value < minimum or value > maximum:
        raise ValidationError(f"Value {value} not in range {minimum} -> {maximum}")


def validate_not_all(**values: bool) -> None:
    collective: str

    if len(values) <= 1:
        collective = ""
    elif len(values) == 2:
        collective = "both"
    else:
        collective = "all"

    keys: str = ""

    index: int
    key: str
    for index, key in enumerate(values.keys()):
        if index != 0:
            if index == len(values) - 1:
                keys += " and "
            else:
                keys += ", "

        keys += key

    if all(values.values()):
        raise ValidationError(f"{keys} cannot {collective}{collective and ' '}be True")


def validate_byte(value: int, /) -> None:
    validate_in_range(value, BYTE_MIN, BYTE_MAX)


def validate_bytes(*values: int) -> None:
    value: int
    for value in values:
        validate_byte(value)


def validate_address(value: int, /) -> None:
    validate_in_range(value, MIN_ADDRESS, MAX_ADDRESS)


def validate_pan_speed(value: int, /) -> None:
    validate_in_range(value, MIN_PAN_SPEED, MAX_PAN_SPEED)


def validate_tilt_speed(value: int, /) -> None:
    validate_in_range(value, MIN_TILT_SPEED, MAX_TILT_SPEED)


def validate_preset_id(value: int, /) -> None:
    validate_in_range(value, MIN_PRESET_ID, MAX_PRESET_ID)


def validate_aux_id(value: int, /) -> None:
    validate_in_range(value, MIN_AUX_ID, MAX_AUX_ID)


def validate_zone_id(value: int, /) -> None:
    validate_in_range(value, MIN_ZONE_ID, MAX_ZONE_ID)


def validate_screen_column(value: int, /) -> None:
    validate_in_range(value, MIN_SCREEN_COLUMN, MAX_SCREEN_COLUMN)


def validate_pattern_id(value: int, /) -> None:
    validate_in_range(value, MIN_PATTERN_ID, MAX_PATTERN_ID)


def validate_zoom_speed(value: int, /) -> None:
    validate_in_range(value, MIN_ZOOM_SPEED, MAX_ZOOM_SPEED)


def validate_focus_speed(value: int, /) -> None:
    validate_in_range(value, MIN_FOCUS_SPEED, MAX_FOCUS_SPEED)
