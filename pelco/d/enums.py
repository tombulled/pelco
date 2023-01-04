from enum import IntEnum

from .constants import (
    D_ECD_ZOOM_SPEED_SLOW,
    D_ECD_ZOOM_SPEED_MEDIUM,
    D_ECD_ZOOM_SPEED_FAST,
    D_ECD_ZOOM_SPEED_FASTEST,
    D_ECD_FOCUS_SPEED_SLOW,
    D_ECD_FOCUS_SPEED_MEDIUM,
    D_ECD_FOCUS_SPEED_FAST,
    D_ECD_FOCUS_SPEED_FASTEST,
    D_ECD_AUTO_FOCUS_AUTO,
    D_ECD_AUTO_FOCUS_OFF,
    D_ECD_AUTO_IRIS_AUTO,
    D_ECD_AUTO_IRIS_OFF,
    D_ECD_AUTO_AGC_AUTO,
    D_ECD_AUTO_AGC_OFF,
    D_ECD_AUTO_BLC_OFF,
    D_ECD_AUTO_BLC_ON,
    D_ECD_AUTO_AWB_ON,
    D_ECD_AUTO_AWB_OFF,
)


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


class ZoomSpeed(IntEnum):
    SLOW: int = D_ECD_ZOOM_SPEED_SLOW
    MEDIUM: int = D_ECD_ZOOM_SPEED_MEDIUM
    FAST: int = D_ECD_ZOOM_SPEED_FAST
    VERY_FAST: int = D_ECD_ZOOM_SPEED_FASTEST


class FocusSpeed(IntEnum):
    SLOW: int = D_ECD_FOCUS_SPEED_SLOW
    MEDIUM: int = D_ECD_FOCUS_SPEED_MEDIUM
    FAST: int = D_ECD_FOCUS_SPEED_FAST
    VERY_FAST: int = D_ECD_FOCUS_SPEED_FASTEST


class AutoFocusMode(IntEnum):
    AUTO: int = D_ECD_AUTO_FOCUS_AUTO
    OFF: int = D_ECD_AUTO_FOCUS_OFF


class AutoIrisMode(IntEnum):
    AUTO: int = D_ECD_AUTO_IRIS_AUTO
    OFF: int = D_ECD_AUTO_IRIS_OFF


class AutomaticGainControlMode(IntEnum):
    AUTO: int = D_ECD_AUTO_AGC_AUTO
    OFF: int = D_ECD_AUTO_AGC_OFF


class BacklightCompensationMode(IntEnum):
    OFF: int = D_ECD_AUTO_BLC_OFF
    ON: int = D_ECD_AUTO_BLC_ON


class AutoWhiteBalanceMode(IntEnum):
    ON: int = D_ECD_AUTO_AWB_ON
    OFF: int = D_ECD_AUTO_AWB_OFF


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


class VersionInformationCommand(IntEnum):
    SOFTWARE_VERSION_NUMBER: int = 0x00
    BUILD_NUMBER: int = 0x02


class VersionInformationResponse(IntEnum):
    SOFTWARE_VERSION_NUMBER: int = 0x01
    BUILD_NUMBER: int = 0x03

    @classmethod
    def for_command(
        cls, command: VersionInformationCommand
    ) -> "VersionInformationResponse":
        return cls(command + 1)
