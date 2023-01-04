from .constants import (
    MAX_LINE_LOCK_PHASE_DELAY,
    MAX_SHUTTER_SPEED,
    MAX_WHITE_BALANCE_MG,
    MAX_WHITE_BALANCE_RB,
    MIN_LINE_LOCK_PHASE_DELAY,
    MIN_SHUTTER_SPEED,
    MIN_WHITE_BALANCE_MG,
    MIN_WHITE_BALANCE_RB,
    UINT8_MAX,
    UINT8_MIN,
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
    UINT16_MIN,
    UINT16_MAX,
)
from .errors import ValidationError


def validate_odd(value: int, /) -> None:
    if value % 2 == 0:
        raise ValidationError(f"Value {value} is not odd")


def validate_even(value: int, /) -> None:
    if value % 2 == 1:
        raise ValidationError(f"Value {value} is not even")


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


def validate_uint8(value: int, /) -> None:
    validate_in_range(value, UINT8_MIN, UINT8_MAX)


def validate_uint16(value: int, /) -> None:
    validate_in_range(value, UINT16_MIN, UINT16_MAX)


def validate_all_uint8(*values: int) -> None:
    value: int
    for value in values:
        validate_uint8(value)


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


def validate_shutter_speed(value: int, /) -> None:
    validate_in_range(value, MIN_SHUTTER_SPEED, MAX_SHUTTER_SPEED)


def validate_line_lock_phase_delay(value: int, /) -> None:
    validate_in_range(value, MIN_LINE_LOCK_PHASE_DELAY, MAX_LINE_LOCK_PHASE_DELAY)


def validate_white_balance_rb(value: int, /) -> None:
    validate_in_range(value, MIN_WHITE_BALANCE_RB, MAX_WHITE_BALANCE_RB)


def validate_white_balance_mg(value: int, /) -> None:
    validate_in_range(value, MIN_WHITE_BALANCE_MG, MAX_WHITE_BALANCE_MG)
