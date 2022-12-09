SYNC: int = 0xFF

MIN_ADDRESS: int = 0x01
MAX_ADDRESS: int = 0xFF
MIN_PRESET: int = 0x01
MAX_PRESET: int = 0xFF  # NOTE: Although up to 0xff supported in spec, MIC only supports up to 0x64 (100 presets)
MIN_TILT_SPEED: int = 0x00
MAX_TILT_SPEED: int = 0x3F
MIN_PAN_SPEED: int = 0x00
MAX_PAN_SPEED: int = 0x40
MIN_AUX_ID: int = 0x01
MAX_AUX_ID: int = 0x08
MIN_ZONE_ID: int = 0x01
MAX_ZONE_ID: int = 0xFF
MIN_SCREEN_COLUMN: int = 0x00
MAX_SCREEN_COLUMN: int = 0x27
MIN_PATTERN_ID: int = 0x00
MAX_PATTERN_ID: int = 0x08
MIN_ZOOM_SPEED: int = 0x00
MAX_ZOOM_SPEED: int = 0x03
MIN_FOCUS_SPEED: int = 0x00
MAX_FOCUS_SPEED: int = 0x03
MIN_AUTO_FOCUS_MODE: int = 0x00
MAX_AUTO_FOCUS_MODE: int = 0x01

SENSE: int = 0b10000000
RESERVED_6: int = 0b01000000
RESERVED_5: int = 0b00100000
SCAN: int = 0b00010000
CAMERA: int = 0b00001000
IRIS_CLOSE: int = 0b00000100
IRIS_OPEN: int = 0b00000010
FOCUS_NEAR: int = 0b00000001

FOCUS_FAR: int = 0b10000000
ZOOM_WIDE: int = 0b01000000
ZOOM_TELE: int = 0b00100000
DOWN: int = 0b00010000
UP: int = 0b00001000
LEFT: int = 0b00000100
RIGHT: int = 0b00000010
RESERVED_0: int = 0b00000001

# Extended Commands
SET_PRESET: int = 0x03
CLEAR_PRESET: int = 0x05
GO_TO_PRESET: int = 0x07
SET_AUXILIARY: int = 0x09
CLEAR_AUXILIARY: int = 0x0B
DUMMY: int = 0x0D
REMOTE_RESET: int = 0x0F
SET_ZONE_START: int = 0x11
SET_ZONE_END: int = 0x13
WRITE_CHARACTER_TO_SCREEN: int = 0x15
CLEAR_SCREEN: int = 0x17
ALARM_ACKNOWLEDGE: int = 0x19
ZONE_SCAN_ON: int = 0x1B
ZONE_SCAN_OFF: int = 0x1D
SET_PATTERN_START: int = 0x1F
SET_PATTERN_STOP: int = 0x21
RUN_PATTERN: int = 0x23
SET_ZOOM_SPEED: int = 0x25
SET_FOCUS_SPEED: int = 0x27
RESET_CAMERA_DEFAULTS: int = 0x29
AUTO_FOCUS_MODE: int = 0x2B
AUTO_IRIS_MODE: int = 0x2D
AGC_MODE: int = 0x2F
BACKLIGHT_COMPENSATION: int = 0x31
AUTO_WHITE_BALANCE: int = 0x33
ENABLE_DEVICE_PHASE_DELAY_MODE: int = 0x35
SET_SHUTTER_SPEED: int = 0x37
ADJUST_LINE_LOCK_PHASE_DELAY: int = 0x39
ADJUST_WHITE_BALANCE_RB: int = 0x3B
ADJUST_WHITE_BALANCE_MG: int = 0x3D
ADJUST_GAIN: int = 0x3F
ADJUST_AUTO_IRIS_LEVEL: int = 0x41
ADJUST_AUTO_IRIS_PEAK_VALUE: int = 0x43
QUERY: int = 0x45
PRESET_SCAN: int = 0x47
SET_ZERO_POSITION: int = 0x49
SET_PAN_POSITION: int = 0x4B
SET_TILT_POSITION: int = 0x4D
SET_ZOOM_POSITION: int = 0x4F
QUERY_PAN_POSITION: int = 0x51
QUERY_TILT_POSITION: int = 0x53
QUERY_ZOOM_POSITION: int = 0x55
DOWNLOAD: int = 0x57
QUERY_PAN_POSITION_RESPONSE: int = 0x59
QUERY_TILT_POSITION_RESPONSE: int = 0x5B
QUERY_ZOOM_POSITION_RESPONSE: int = 0x5D
SET_MAGNIFICATION: int = 0x5F
QUERY_MAGNIFICATION: int = 0x61
QUERY_MAGNIFICATION_RESPONSE: int = 0x63
ACTIVATE_ECHO_MODE: int = 0x65
SET_REMOTE_BAUD_RATE: int = 0x67
START_DOWNLOAD: int = 0x69
QUERY_DEVICE_TYPE: int = 0x6B
QUERY_DEVICE_TYPE_RESPONSE: int = 0x6D
QUERY_DIAGNOSTIC_INFORMATION: int = 0x6F
QUERY_DIAGNOSTIC_INFORMATION_RESPONSE: int = 0x71
VERSION_INFORMATION_MACRO_OPCODE: int = 0x73
EVEREST_MACRO_OPCODE: int = 0x75
TIMESET_MACRO_OPCODE: int = 0x77
SCREEN_MOVE: int = 0x79

# Predefined Presets
PRESET_FLIP: int = 0x21
PRESET_ZERO: int = 0x22
PRESET_AUX1: int = 0x54
PRESET_AUX2: int = 0x55
PRESET_WIPER: int = 0x56
PRESET_WASHER: int = 0x57
PRESET_IR_FILTER_IN: int = 0x58
PRESET_IR_FILTER_OUT: int = 0x59
PRESET_MANUAL_LEFT_LIMIT: int = 0x5A
PRESET_MANUAL_RIGHT_LIMIT: int = 0x5B
PRESET_SCAN_LEFT_LIMIT: int = 0x5C
PRESET_SCAN_RIGHT_LIMIT: int = 0x5D
PRESET_RESET: int = 0x5E
PRESET_MENU_MODE: int = 0x5F
PRESET_STOP_SCAN: int = 0x60
PRESET_RANDOM_SCAN: int = 0x61
PRESET_FRAME_SCAN: int = 0x62
PRESET_AUTO_SCAN: int = 0x63
