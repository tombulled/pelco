from dataclasses import dataclass

from .constants import (
    BYTE_MAX,
    BYTE_SIZE,
    D_C_CAMERA,
    D_C_DOWN,
    D_C_FOCUS_FAR,
    D_C_FOCUS_NEAR,
    D_C_IRIS_CLOSE,
    D_C_IRIS_OPEN,
    D_C_LEFT,
    D_C_RIGHT,
    D_C_SCAN,
    D_C_SENSE,
    D_C_UP,
    D_C_ZOOM_TELE,
    D_C_ZOOM_WIDE,
    D_EC_ADJUST_AI_LEVEL,
    D_EC_ADJUST_AI_PEAK,
    D_EC_ADJUST_GAIN,
    D_EC_ADJUST_MG_WB,
    D_EC_ADJUST_PHASE,
    D_EC_ADJUST_RB_WB,
    D_EC_AGC,
    D_EC_AUTO_FOCUS,
    D_EC_AUTO_IRIS,
    D_EC_AWB,
    D_EC_BLC,
    D_EC_CAMERA_RESET,
    D_EC_CLEAR_AUX,
    D_EC_CLEAR_PRESET,
    D_EC_DEVICE_PHASE,
    D_EC_END_RECORD,
    D_EC_EVEREST,
    D_EC_FOCUS_SPEED,
    D_EC_MOVE_PRESET,
    D_EC_QUERY,
    D_EC_QUERY_DEV_TYPE,
    D_EC_QUERY_DIAG_INFO,
    D_EC_QUERY_MAG,
    D_EC_QUERY_PAN,
    D_EC_QUERY_TILT,
    D_EC_QUERY_ZOOM,
    D_EC_RESET,
    D_EC_SET_AUX,
    D_EC_SET_PAN,
    D_EC_SET_PRESET,
    D_EC_SET_TILT,
    D_EC_SET_ZERO,
    D_EC_SHUTTER_SPEED,
    D_EC_START_PLAY,
    D_EC_START_RECORD,
    D_EC_VERSION_INFO,
    D_EC_WRITE_CHAR,
    D_EC_ZONE_END,
    D_EC_ZONE_OFF,
    D_EC_ZONE_ON,
    D_EC_ZONE_START,
    D_EC_ZOOM,
    D_EC_ZOOM_SPEED,
    D_ECS_SET_AUX_LED,
    D_ECS_SET_AUX_RELAY,
    DEFAULT_ADDRESS,
    MAX_ADJUST_AUTO_IRIS_LEVEL,
    MAX_ADJUST_AUTO_IRIS_LEVEL_MODE,
    MAX_ADJUST_AUTO_IRIS_PEAK_VALUE,
    MAX_ADJUST_AUTO_IRIS_PEAK_VALUE_MODE,
    MAX_ADJUST_GAIN,
    MAX_ADJUST_GAIN_MODE,
    MAX_AGC_MODE,
    MAX_AUTO_FOCUS_MODE,
    MAX_AUTO_IRIS_MODE,
    MAX_AUTO_WHITE_BALANCE_MODE,
    MAX_BACKLIGHT_COMPENSATION_MODE,
    MAX_EVEREST_MACRO_SUB_OPCODE,
    MAX_LINE_LOCK_PHASE_DELAY,
    MAX_LINE_LOCK_PHASE_DELAY_MODE,
    MAX_PAN_POSITION,
    MAX_QUERY_TYPE,
    MAX_SHUTTER_SPEED,
    MAX_TILT_POSITION,
    MAX_VERSION_INFORMATION_MACRO_SUB_OPCODE,
    MAX_WHITE_BALANCE_MG,
    MAX_WHITE_BALANCE_MG_MODE,
    MAX_WHITE_BALANCE_RB,
    MAX_WHITE_BALANCE_RB_MODE,
    MAX_ZOOM_POSITION,
    MIN_ADJUST_AUTO_IRIS_LEVEL,
    MIN_ADJUST_AUTO_IRIS_LEVEL_MODE,
    MIN_ADJUST_AUTO_IRIS_PEAK_VALUE,
    MIN_ADJUST_AUTO_IRIS_PEAK_VALUE_MODE,
    MIN_ADJUST_GAIN,
    MIN_ADJUST_GAIN_MODE,
    MIN_AGC_MODE,
    MIN_AUTO_FOCUS_MODE,
    MIN_AUTO_IRIS_MODE,
    MIN_AUTO_WHITE_BALANCE_MODE,
    MIN_BACKLIGHT_COMPENSATION_MODE,
    MIN_EVEREST_MACRO_SUB_OPCODE,
    MIN_LINE_LOCK_PHASE_DELAY,
    MIN_LINE_LOCK_PHASE_DELAY_MODE,
    MIN_PAN_POSITION,
    MIN_QUERY_TYPE,
    MIN_SHUTTER_SPEED,
    MIN_TILT_POSITION,
    MIN_VERSION_INFORMATION_MACRO_SUB_OPCODE,
    MIN_WHITE_BALANCE_MG,
    MIN_WHITE_BALANCE_MG_MODE,
    MIN_WHITE_BALANCE_RB,
    MIN_WHITE_BALANCE_RB_MODE,
    MIN_ZOOM_POSITION,
    PRESET_FLIP,
    PRESET_ZERO,
)
from .models import SendCommandModel
from .validators import (
    validate_address,
    validate_aux_id,
    validate_byte,
    validate_bytes,
    validate_focus_speed,
    validate_not_all,
    validate_pan_speed,
    validate_pattern_id,
    validate_preset_id,
    validate_screen_column,
    validate_tilt_speed,
    validate_zone_id,
    validate_zoom_speed,
)


@dataclass
class CommandFactory:
    address: int

    def __init__(self, address: int = DEFAULT_ADDRESS):
        validate_address(address)

        self.address = address

    def _command(
        self,
        command_1: int = 0x00,
        command_2: int = 0x00,
        data_1: int = 0x00,
        data_2: int = 0x00,
    ) -> SendCommandModel:
        validate_bytes(command_1, command_2, data_1, data_2)

        return SendCommandModel(
            address=self.address,
            command_1=command_1,
            command_2=command_2,
            data_1=data_1,
            data_2=data_2,
        )

    def standard(
        self,
        *,
        sense: bool = False,
        scan: bool = False,
        camera: bool = False,
        iris_close: bool = False,
        iris_open: bool = False,
        focus_near: bool = False,
        focus_far: bool = False,
        zoom_wide: bool = False,
        zoom_tele: bool = False,
        down: bool = False,
        up: bool = False,
        left: bool = False,
        right: bool = False,
        pan_speed: int = 0,
        tilt_speed: int = 0,
    ) -> SendCommandModel:
        validate_pan_speed(pan_speed)
        validate_tilt_speed(tilt_speed)
        validate_not_all(iris_close=iris_close, iris_open=iris_open)
        validate_not_all(focus_near=focus_near, focus_far=focus_far)
        validate_not_all(zoom_wide=zoom_wide, zoom_tele=zoom_tele)
        validate_not_all(up=up, down=down)
        validate_not_all(left=left, right=right)

        command_1: int = int(
            (sense and D_C_SENSE)
            | (scan and D_C_SCAN)
            | (camera and D_C_CAMERA)
            | (iris_close and D_C_IRIS_CLOSE)
            | (iris_open and D_C_IRIS_OPEN)
            | (focus_near and D_C_FOCUS_NEAR)
        )
        command_2: int = int(
            (focus_far and D_C_FOCUS_FAR)
            | (zoom_wide and D_C_ZOOM_WIDE)
            | (zoom_tele and D_C_ZOOM_TELE)
            | (down and D_C_DOWN)
            | (up and D_C_UP)
            | (left and D_C_LEFT)
            | (right and D_C_RIGHT)
        )

        return self._command(
            command_1=command_1,
            command_2=command_2,
            data_1=pan_speed,
            data_2=tilt_speed,
        )

    def stop(self) -> SendCommandModel:
        return self.standard()

    def camera_on(self) -> SendCommandModel:
        return self.standard(camera=True, sense=True)

    def camera_off(self) -> SendCommandModel:
        return self.standard(camera=True)

    def scan_auto(self) -> SendCommandModel:
        return self.standard(scan=True, sense=True)

    def scan_manual(self) -> SendCommandModel:
        return self.standard(scan=True)

    def iris_close(self) -> SendCommandModel:
        return self.standard(iris_close=True)

    def iris_open(self) -> SendCommandModel:
        return self.standard(iris_open=True)

    def pan_right(self, speed: int) -> SendCommandModel:
        return self.standard(right=True, pan_speed=speed)

    def pan_left(self, speed: int) -> SendCommandModel:
        return self.standard(left=True, pan_speed=speed)

    def tilt_up(self, speed: int) -> SendCommandModel:
        return self.standard(up=True, tilt_speed=speed)

    def tilt_down(self, speed: int) -> SendCommandModel:
        return self.standard(down=True, tilt_speed=speed)

    def zoom_tele(self) -> SendCommandModel:
        return self.standard(zoom_tele=True)

    def zoom_wide(self) -> SendCommandModel:
        return self.standard(zoom_wide=True)

    def focus_far(self) -> SendCommandModel:
        return self.standard(focus_far=True)

    def focus_near(self) -> SendCommandModel:
        return self.standard(focus_near=True)

    def set_preset(self, preset_id: int) -> SendCommandModel:
        validate_preset_id(preset_id)

        return self._command(
            command_2=D_EC_SET_PRESET,
            data_2=preset_id,
        )

    def clear_preset(self, preset_id: int) -> SendCommandModel:
        """
        Clears the requested preset's information from the camera system.
        Pre-assigned presets may not be cleared. It is not necessary to clear a
        preset before setting it.
        """

        validate_preset_id(preset_id)

        return self._command(
            command_2=D_EC_CLEAR_PRESET,
            data_2=preset_id,
        )

    def go_to_preset(self, preset_id: int) -> SendCommandModel:
        """
        Causes the camera unit to move, at preset speed, to the requested position.
        """

        validate_preset_id(preset_id)

        return self._command(
            command_2=D_EC_MOVE_PRESET,
            data_2=preset_id,
        )

    def flip_180_about(self) -> SendCommandModel:
        return self.go_to_preset(PRESET_FLIP)

    def go_to_zero_pan(self) -> SendCommandModel:
        return self.go_to_preset(PRESET_ZERO)

    def set_auxiliary_relay(self, aux_id: int) -> SendCommandModel:
        validate_aux_id(aux_id)

        return self._command(
            command_1=D_ECS_SET_AUX_RELAY,
            command_2=D_EC_SET_AUX,
            data_2=aux_id,
        )

    def set_auxiliary_led(self, led: int, rate: int) -> SendCommandModel:
        validate_byte(led)
        validate_byte(rate)

        return self._command(
            command_1=D_ECS_SET_AUX_LED,
            command_2=D_EC_SET_AUX,
            data_1=rate,
            data_2=led,
        )

    def clear_auxiliary(self, aux_id: int) -> SendCommandModel:
        validate_aux_id(aux_id)

        return self._command(
            command_2=D_EC_CLEAR_AUX,
            data_2=aux_id,
        )

    # TODO: dummy

    def remote_reset(self) -> SendCommandModel:
        """
        This command resets the system. It will take several seconds before the
        system is ready to resume normal operation. This is the same as turning
        the system off and then back on.
        """

        return self._command(
            command_2=D_EC_RESET,
        )

    def set_zone_start(self, zone_id: int) -> SendCommandModel:
        validate_zone_id(zone_id)

        return self._command(
            command_2=D_EC_ZONE_START,
            data_2=zone_id,
        )

    def set_zone_end(self, zone_id: int) -> SendCommandModel:
        validate_zone_id(zone_id)

        return self._command(
            command_2=D_EC_ZONE_END,
            data_2=zone_id,
        )

    def write_character_to_screen(
        self, screen_column: int, ascii_char: int
    ) -> SendCommandModel:
        validate_screen_column(screen_column)
        validate_byte(ascii_char)

        return self._command(
            command_2=D_EC_WRITE_CHAR,
            data_1=screen_column,
            data_2=ascii_char,
        )

    def zone_scan_on(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_ZONE_ON,
        )

    def zone_scan_off(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_ZONE_OFF,
        )

    def set_pattern_start(self, pattern_id: int) -> SendCommandModel:
        validate_pattern_id(pattern_id)

        return self._command(
            command_2=D_EC_START_RECORD,
            data_2=pattern_id,
        )

    def set_pattern_end(self, pattern_id: int) -> SendCommandModel:
        validate_pattern_id(pattern_id)

        return self._command(
            command_2=D_EC_END_RECORD,
            data_2=pattern_id,
        )

    def run_pattern(self, pattern_id: int) -> SendCommandModel:
        validate_pattern_id(pattern_id)

        return self._command(
            command_2=D_EC_START_PLAY,
            data_2=pattern_id,
        )

    def set_zoom_speed(self, zoom_speed: int) -> SendCommandModel:
        validate_zoom_speed(zoom_speed)

        return self._command(
            command_2=D_EC_ZOOM_SPEED,
            data_2=zoom_speed,
        )

    def set_focus_speed(self, focus_speed: int) -> SendCommandModel:
        validate_focus_speed(focus_speed)

        return self._command(
            command_2=D_EC_FOCUS_SPEED,
            data_2=focus_speed,
        )

    def reset_camera_to_defaults(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_CAMERA_RESET,
        )

    def set_auto_focus_mode(self, auto_focus_mode: int) -> SendCommandModel:
        assert MIN_AUTO_FOCUS_MODE <= auto_focus_mode <= MAX_AUTO_FOCUS_MODE

        return self._command(
            command_2=D_EC_AUTO_FOCUS,
            data_2=auto_focus_mode,
        )

    def set_auto_iris_mode(self, auto_iris_mode: int) -> SendCommandModel:
        assert MIN_AUTO_IRIS_MODE <= auto_iris_mode <= MAX_AUTO_IRIS_MODE

        return self._command(
            command_2=D_EC_AUTO_IRIS,
            data_2=auto_iris_mode,
        )

    def set_agc_mode(self, agc_mode: int) -> SendCommandModel:
        assert MIN_AGC_MODE <= agc_mode <= MAX_AGC_MODE

        return self._command(
            command_2=D_EC_AGC,
            data_2=agc_mode,
        )

    def set_backlight_compensation_mode(
        self, backlight_compensation_mode: int
    ) -> SendCommandModel:
        assert (
            MIN_BACKLIGHT_COMPENSATION_MODE
            <= backlight_compensation_mode
            <= MAX_BACKLIGHT_COMPENSATION_MODE
        )

        return self._command(
            command_2=D_EC_BLC,
            data_2=backlight_compensation_mode,
        )

    def set_auto_white_balance_mode(
        self, auto_white_balance_mode: int
    ) -> SendCommandModel:
        assert (
            MIN_AUTO_WHITE_BALANCE_MODE
            <= auto_white_balance_mode
            <= MAX_AUTO_WHITE_BALANCE_MODE
        )

        return self._command(
            command_2=D_EC_AWB,
            data_2=auto_white_balance_mode,
        )

    def enable_device_phase_delay_mode(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_DEVICE_PHASE,
        )

    def set_shutter_speed(self, shutter_speed: int) -> SendCommandModel:
        assert MIN_SHUTTER_SPEED <= shutter_speed <= MAX_SHUTTER_SPEED

        shutter_speed_msb: int = (shutter_speed >> BYTE_SIZE) & BYTE_MAX
        shutter_speed_lsb: int = shutter_speed & BYTE_MAX

        return self._command(
            command_2=D_EC_SHUTTER_SPEED,
            data_1=shutter_speed_msb,
            data_2=shutter_speed_lsb,
        )

    def adjust_line_lock_phase_delay(
        self, line_lock_phase_delay_mode: int, line_lock_phase_delay: int
    ) -> SendCommandModel:
        assert (
            MIN_LINE_LOCK_PHASE_DELAY_MODE
            <= line_lock_phase_delay_mode
            <= MAX_LINE_LOCK_PHASE_DELAY_MODE
        )
        assert (
            MIN_LINE_LOCK_PHASE_DELAY
            <= line_lock_phase_delay
            <= MAX_LINE_LOCK_PHASE_DELAY
        )

        line_lock_phase_delay_msb: int = (line_lock_phase_delay >> BYTE_SIZE) & BYTE_MAX
        line_lock_phase_delay_lsb: int = line_lock_phase_delay & BYTE_MAX

        return self._command(
            command_1=line_lock_phase_delay_mode,
            command_2=D_EC_ADJUST_PHASE,
            data_1=line_lock_phase_delay_msb,
            data_2=line_lock_phase_delay_lsb,
        )

    def adjust_white_balance_rb(
        self, white_balance_mode: int, white_balance: int
    ) -> SendCommandModel:
        assert (
            MIN_WHITE_BALANCE_RB_MODE <= white_balance_mode <= MAX_WHITE_BALANCE_RB_MODE
        )
        assert MIN_WHITE_BALANCE_RB <= white_balance <= MAX_WHITE_BALANCE_RB

        white_balance_msb: int = (white_balance >> BYTE_SIZE) & BYTE_MAX
        white_balance_lsb: int = white_balance & BYTE_MAX

        return self._command(
            command_1=white_balance_mode,
            command_2=D_EC_ADJUST_RB_WB,
            data_1=white_balance_msb,
            data_2=white_balance_lsb,
        )

    def adjust_white_balance_mg(
        self, white_balance_mode: int, white_balance: int
    ) -> SendCommandModel:
        assert (
            MIN_WHITE_BALANCE_MG_MODE <= white_balance_mode <= MAX_WHITE_BALANCE_MG_MODE
        )
        assert MIN_WHITE_BALANCE_MG <= white_balance <= MAX_WHITE_BALANCE_MG

        white_balance_msb: int = (white_balance >> BYTE_SIZE) & BYTE_MAX
        white_balance_lsb: int = white_balance & BYTE_MAX

        return self._command(
            command_1=white_balance_mode,
            command_2=D_EC_ADJUST_MG_WB,
            data_1=white_balance_msb,
            data_2=white_balance_lsb,
        )

    def adjust_gain(self, adjust_gain_mode: int, adjust_gain: int) -> SendCommandModel:
        assert MIN_ADJUST_GAIN_MODE <= adjust_gain_mode <= MAX_ADJUST_GAIN_MODE
        assert MIN_ADJUST_GAIN <= adjust_gain <= MAX_ADJUST_GAIN

        adjust_gain_msb: int = (adjust_gain >> BYTE_SIZE) & BYTE_MAX
        adjust_gain_lsb: int = adjust_gain & BYTE_MAX

        return self._command(
            command_1=adjust_gain_mode,
            command_2=D_EC_ADJUST_GAIN,
            data_1=adjust_gain_msb,
            data_2=adjust_gain_lsb,
        )

    def adjust_auto_iris_level(
        self, auto_iris_level_mode: int, auto_iris_level: int
    ) -> SendCommandModel:
        assert (
            MIN_ADJUST_AUTO_IRIS_LEVEL_MODE
            <= auto_iris_level_mode
            <= MAX_ADJUST_AUTO_IRIS_LEVEL_MODE
        )
        assert (
            MIN_ADJUST_AUTO_IRIS_LEVEL <= auto_iris_level <= MAX_ADJUST_AUTO_IRIS_LEVEL
        )

        auto_iris_level_msb: int = (auto_iris_level >> BYTE_SIZE) & BYTE_MAX
        auto_iris_level_lsb: int = auto_iris_level & BYTE_MAX

        return self._command(
            command_1=auto_iris_level_mode,
            command_2=D_EC_ADJUST_AI_LEVEL,
            data_1=auto_iris_level_msb,
            data_2=auto_iris_level_lsb,
        )

    def adjust_auto_iris_peak_value(
        self, auto_iris_peak_value_mode: int, auto_iris_peak_value: int
    ) -> SendCommandModel:
        assert (
            MIN_ADJUST_AUTO_IRIS_PEAK_VALUE_MODE
            <= auto_iris_peak_value_mode
            <= MAX_ADJUST_AUTO_IRIS_PEAK_VALUE_MODE
        )
        assert (
            MIN_ADJUST_AUTO_IRIS_PEAK_VALUE
            <= auto_iris_peak_value
            <= MAX_ADJUST_AUTO_IRIS_PEAK_VALUE
        )

        auto_iris_peak_value_msb: int = (auto_iris_peak_value >> BYTE_SIZE) & BYTE_MAX
        auto_iris_peak_value_lsb: int = auto_iris_peak_value & BYTE_MAX

        return self._command(
            command_1=auto_iris_peak_value_mode,
            command_2=D_EC_ADJUST_AI_PEAK,
            data_1=auto_iris_peak_value_msb,
            data_2=auto_iris_peak_value_lsb,
        )

    def query(self, query_type: int) -> SendCommandModel:
        assert MIN_QUERY_TYPE <= query_type <= MAX_QUERY_TYPE

        # This command does not utilise the address field.
        # This is so that the address of a unit may be determined programatically.
        return SendCommandModel(
            # address=self.address,
            command_1=query_type,
            command_2=D_EC_QUERY,
        )

    # TODO: preset_scan

    def set_zero_position(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_SET_ZERO,
        )

    def set_pan_position(self, pan_position: int) -> SendCommandModel:
        assert MIN_PAN_POSITION <= pan_position <= MAX_PAN_POSITION

        pan_msb: int = (pan_position >> BYTE_SIZE) & BYTE_MAX
        pan_lsb: int = pan_position & BYTE_MAX

        return self._command(
            command_2=D_EC_SET_PAN,
            data_1=pan_msb,
            data_2=pan_lsb,
        )

    def set_tilt_position(self, tilt_position: int) -> SendCommandModel:
        assert MIN_TILT_POSITION <= tilt_position <= MAX_TILT_POSITION

        tilt_msb: int = (tilt_position >> BYTE_SIZE) & BYTE_MAX
        tilt_lsb: int = tilt_position & BYTE_MAX

        return self._command(
            command_2=D_EC_SET_TILT,
            data_1=tilt_msb,
            data_2=tilt_lsb,
        )

    def set_zoom_position(self, zoom_position: int) -> SendCommandModel:
        assert MIN_ZOOM_POSITION <= zoom_position <= MAX_ZOOM_POSITION

        zoom_msb: int = (zoom_position >> BYTE_SIZE) & BYTE_MAX
        zoom_lsb: int = zoom_position & BYTE_MAX

        return self._command(
            command_2=D_EC_ZOOM,
            data_1=zoom_msb,
            data_2=zoom_lsb,
        )

    def query_pan_position(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_QUERY_PAN,
        )

    def query_tilt_position(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_QUERY_TILT,
        )

    def query_zoom_position(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_QUERY_ZOOM,
        )

    # TODO: prepare_for_download
    # TODO: set_magnification

    def query_magnification(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_QUERY_MAG,
        )

    # TODO: activate_echo_mode
    # TODO: set_remote_baud_rate
    # TODO: start_download

    def query_device_type(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_QUERY_DEV_TYPE,
        )

    def query_diagnostic_information(self) -> SendCommandModel:
        return self._command(
            command_2=D_EC_QUERY_DIAG_INFO,
        )

    def version_information_macro(self, command: int) -> SendCommandModel:
        assert command in list(
            range(
                MIN_VERSION_INFORMATION_MACRO_SUB_OPCODE,
                MAX_VERSION_INFORMATION_MACRO_SUB_OPCODE + 1,
                2,
            )
        )

        return self._command(
            command_1=command,
            command_2=D_EC_VERSION_INFO,
        )

    def everest_macro(
        self, command: int, *, data_1: int = 0x00, data_2: int = 0x00
    ) -> SendCommandModel:
        assert command in list(
            range(MIN_EVEREST_MACRO_SUB_OPCODE, MAX_EVEREST_MACRO_SUB_OPCODE + 1, 2)
        )

        return self._command(
            command_1=command,
            command_2=D_EC_EVEREST,
            data_1=data_1,
            data_2=data_2,
        )

    # TODO: time_commands
    # TODO: screen_move
