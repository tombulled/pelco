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


class AutoIrisMode(IntEnum):
    AUTO: int = 0x00
    OFF: int = 0x01


class AutomaticGainControlMode(IntEnum):
    AUTO: int = 0x00
    OFF: int = 0x01


class BacklightCompensationMode(IntEnum):
    OFF: int = 0x00
    ON: int = 0x01


class AutoWhiteBalanceMode(IntEnum):
    OFF: int = 0x01
    ON: int = 0x02


class PanPosition(IntEnum):
    D_0: int = 0
    D_45: int = 45 * 100
    D_90: int = 90 * 100
    D_135: int = 135 * 100
    D_180: int = 180 * 100
    D_225: int = 225 * 100
    D_270: int = 270 * 100
    D_315: int = 315 * 100
    D_360: int = 360 * 100 - 1


class TiltPosition(IntEnum):
    D_0: int = 0
    D_45: int = 45 * 100
    D_90: int = 90 * 100
    D_135: int = 135 * 100
    D_180: int = 180 * 100
    D_225: int = 225 * 100
    D_270: int = 270 * 100
    D_315: int = 315 * 100
    D_360: int = 360 * 100 - 1


class LineLockPhaseDelayMode(IntEnum):
    NEW: int = 0x00
    DELTA: int = 0x01


class WhiteBalanceRBMode(IntEnum):
    NEW: int = 0x00
    DELTA: int = 0x01


class WhiteBalanceMGMode(IntEnum):
    NEW: int = 0x00
    DELTA: int = 0x01


class AdjustGainMode(IntEnum):
    NEW: int = 0x00
    DELTA: int = 0x01


class AdjustAutoIrisLevelMode(IntEnum):
    NEW: int = 0x00
    DELTA: int = 0x01


class AdjustAutoIrisPeakValueMode(IntEnum):
    NEW: int = 0x00
    DELTA: int = 0x01
