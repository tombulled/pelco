from enum import IntEnum


class PanSpeed(IntEnum):
    VERY_SLOW: int = 0x00
    SLOW: int = 0x0F
    MEDIUM: int = 0x1F
    FAST: int = 0x2F
    VERY_FAST = 0x3F
    TURBO: int = 0x40


class TiltSpeed(IntEnum):
    VERY_SLOW: int = 0x00
    SLOW: int = 0x0F
    MEDIUM: int = 0x1F
    FAST: int = 0x2F
    VERY_FAST = 0x3F


class ZoomSpeed(IntEnum):
    SLOW: int = 0x00
    MEDIUM: int = 0x01
    FAST: int = 0x02
    FASTEST: int = 0x03


class FocusSpeed(IntEnum):
    SLOW: int = 0x00
    MEDIUM: int = 0x01
    FAST: int = 0x02
    FASTEST: int = 0x03


class AutoFocusMode(IntEnum):
    AUTO: int = 0x00
    OFF: int = 0x01
