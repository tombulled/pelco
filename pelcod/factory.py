from dataclasses import dataclass
from typing import Final

from . import utils
from .constants import (
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
    D_EC_DUMMY_1,
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
    D_ECD_AUTO_AGC_AUTO,
    D_ECD_AUTO_AGC_OFF,
    D_ECD_AUTO_AWB_OFF,
    D_ECD_AUTO_AWB_ON,
    D_ECD_AUTO_BLC_OFF,
    D_ECD_AUTO_BLC_ON,
    D_ECD_AUTO_FOCUS_AUTO,
    D_ECD_AUTO_FOCUS_OFF,
    D_ECD_AUTO_IRIS_AUTO,
    D_ECD_AUTO_IRIS_OFF,
    D_ECS_ADJUST_MG_WB_DELTA,
    D_ECS_ADJUST_MG_WB_NEW,
    D_ECS_ADJUST_PHASE_DELTA,
    D_ECS_ADJUST_PHASE_NEW,
    D_ECS_ADJUST_RB_WB_DELTA,
    D_ECS_ADJUST_RB_WB_NEW,
    D_ECS_CLEAR_AUX_LED,
    D_ECS_CLEAR_AUX_RELAY,
    D_ECS_SET_AUX_LED,
    D_ECS_SET_AUX_RELAY,
    DEFAULT_ADDRESS,
    MAX_ADJUST_AUTO_IRIS_LEVEL,
    MAX_ADJUST_AUTO_IRIS_LEVEL_MODE,
    MAX_ADJUST_AUTO_IRIS_PEAK_VALUE,
    MAX_ADJUST_AUTO_IRIS_PEAK_VALUE_MODE,
    MAX_ADJUST_GAIN,
    MAX_ADJUST_GAIN_MODE,
    MAX_EVEREST_MACRO_SUB_OPCODE,
    MAX_PAN_POSITION,
    MAX_QUERY_TYPE,
    MAX_TILT_POSITION,
    MAX_VERSION_INFORMATION_MACRO_SUB_OPCODE,
    MAX_ZOOM_POSITION,
    MIN_ADJUST_AUTO_IRIS_LEVEL,
    MIN_ADJUST_AUTO_IRIS_LEVEL_MODE,
    MIN_ADJUST_AUTO_IRIS_PEAK_VALUE,
    MIN_ADJUST_AUTO_IRIS_PEAK_VALUE_MODE,
    MIN_ADJUST_GAIN,
    MIN_ADJUST_GAIN_MODE,
    MIN_EVEREST_MACRO_SUB_OPCODE,
    MIN_PAN_POSITION,
    MIN_QUERY_TYPE,
    MIN_TILT_POSITION,
    MIN_VERSION_INFORMATION_MACRO_SUB_OPCODE,
    MIN_ZOOM_POSITION,
    UINT8_MAX,
    UINT8_SIZE,
    UNSET,
)
from .models import PelcoDCommand
from .validators import (
    validate_address,
    validate_all_uint8,
    validate_aux_id,
    validate_focus_speed,
    validate_line_lock_phase_delay,
    validate_not_all,
    validate_odd,
    validate_pan_speed,
    validate_pattern_id,
    validate_preset_id,
    validate_screen_column,
    validate_shutter_speed,
    validate_tilt_speed,
    validate_uint8,
    validate_uint16,
    validate_white_balance_mg,
    validate_white_balance_rb,
    validate_zone_id,
    validate_zoom_speed,
)


@dataclass(init=False)
class PelcoDCommandFactory:
    address: Final[int]

    def __init__(self, address: int = DEFAULT_ADDRESS) -> None:
        validate_address(address)

        self.address = address

    def _command(
        self,
        command_1: int = UNSET,
        command_2: int = UNSET,
        data_1: int = UNSET,
        data_2: int = UNSET,
    ) -> PelcoDCommand:
        validate_all_uint8(command_1, command_2, data_1, data_2)

        return PelcoDCommand(
            address=self.address,
            command_1=command_1,
            command_2=command_2,
            data_1=data_1,
            data_2=data_2,
        )

    def _standard(
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
        pan_speed: int = UNSET,
        tilt_speed: int = UNSET,
    ) -> PelcoDCommand:
        validate_not_all(iris_close=iris_close, iris_open=iris_open)
        validate_not_all(focus_near=focus_near, focus_far=focus_far)
        validate_not_all(zoom_wide=zoom_wide, zoom_tele=zoom_tele)
        validate_not_all(up=up, down=down)
        validate_not_all(left=left, right=right)
        validate_pan_speed(pan_speed)
        validate_tilt_speed(tilt_speed)

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

    def _extended(
        self,
        opcode: int,
        sub_opcode: int = UNSET,
        data: int = UNSET,
    ):
        validate_uint8(opcode)
        validate_odd(opcode)
        validate_uint8(sub_opcode)
        validate_uint16(data)

        data_1: int
        data_2: int
        data_1, data_2 = utils.sep_uint16(data)

        return self._command(
            command_1=sub_opcode,
            command_2=opcode,
            data_1=data_1,
            data_2=data_2,
        )

    def stop(self) -> PelcoDCommand:
        return self._standard()

    def camera_on(self) -> PelcoDCommand:
        return self._standard(camera=True, sense=True)

    def camera_off(self) -> PelcoDCommand:
        return self._standard(camera=True)

    def scan_auto(self) -> PelcoDCommand:
        return self._standard(scan=True, sense=True)

    def scan_manual(self) -> PelcoDCommand:
        return self._standard(scan=True)

    def iris_close(self) -> PelcoDCommand:
        return self._standard(iris_close=True)

    def iris_open(self) -> PelcoDCommand:
        return self._standard(iris_open=True)

    def pan_right(self, speed: int) -> PelcoDCommand:
        return self._standard(right=True, pan_speed=speed)

    def pan_left(self, speed: int) -> PelcoDCommand:
        return self._standard(left=True, pan_speed=speed)

    def tilt_up(self, speed: int) -> PelcoDCommand:
        return self._standard(up=True, tilt_speed=speed)

    def tilt_down(self, speed: int) -> PelcoDCommand:
        return self._standard(down=True, tilt_speed=speed)

    def zoom_tele(self) -> PelcoDCommand:
        return self._standard(zoom_tele=True)

    def zoom_wide(self) -> PelcoDCommand:
        return self._standard(zoom_wide=True)

    def focus_far(self) -> PelcoDCommand:
        return self._standard(focus_far=True)

    def focus_near(self) -> PelcoDCommand:
        return self._standard(focus_near=True)

    def set_preset(self, preset_id: int) -> PelcoDCommand:
        """
        When this command is issued, the current pan, tilt, focus, and zoom
        positions are saved for the preset number specified in the command and
        the label for that preset becomes whatever is currently on the second
        video line.

        Usually this command will cause the camera system to remember where it
        is currently pointing. Other times it will cause a specific action to
        occur. The most common of specific action is a menu call command
        with either SET PRESET 95 (or SET PRESET 28 in 32 preset mode).

        Pre-assigned presets may not be used for position setting. If an attempt
        to do so is done, then the command is ignored with a General Reply being
        returned. The pre-assigned presets may be determined by using
        QUERY DEFINED PRESETS and its reply of QUERY DEFINED PRESETS RESPONSE.
        """

        validate_preset_id(preset_id)

        return self._extended(D_EC_SET_PRESET, data=preset_id)

    def clear_preset(self, preset_id: int) -> PelcoDCommand:
        """
        Clears the requested preset's information from the camera system.
        Pre-assigned presets may not be cleared. It is not necessary to clear a
        preset before setting it.
        """

        validate_preset_id(preset_id)

        return self._extended(D_EC_CLEAR_PRESET, data=preset_id)

    def move_preset(self, preset_id: int) -> PelcoDCommand:
        """
        Causes the camera unit to move, at preset speed, to the requested position.

        When a move to preset command is received, the preset position stored for
        the preset number specified in the command is checked. If the position
        is not valid, the command is ignored. Otherwise the unit moves to the
        preset pan, tilt, zoom, and focus positions. Once the preset has been
        reached, the preset label is displayed on the second video line or where
        it has been moved through use of the set 95 menu system.

        If any command which causes motion is received during a move to preset,
        the move will be aborted and the new command will start. These commands
        are: a motion command, or another move to preset command. Also, if the
        move is not completed within a timeout period, the move is aborted and
        motion is stopped.
        """

        validate_preset_id(preset_id)

        return self._extended(D_EC_MOVE_PRESET, data=preset_id)

    def set_aux_relay(self, aux_id: int) -> PelcoDCommand:
        validate_aux_id(aux_id)

        return self._extended(
            opcode=D_EC_SET_AUX,
            sub_opcode=D_ECS_SET_AUX_RELAY,
            data=aux_id,
        )

    def set_aux_led(self, led: int, rate: int) -> PelcoDCommand:
        validate_uint8(led)
        validate_uint8(rate)

        return self._command(
            command_1=D_ECS_SET_AUX_LED,
            command_2=D_EC_SET_AUX,
            data_1=rate,
            data_2=led,
        )

    def clear_aux_relay(self, aux_id: int) -> PelcoDCommand:
        """
        Causes an auxiliary function in the camera unit to be deactivated (Relay)
        """

        validate_aux_id(aux_id)

        return self._extended(
            opcode=D_EC_CLEAR_AUX,
            sub_opcode=D_ECS_CLEAR_AUX_RELAY,
            data=aux_id,
        )

    def clear_aux_led(self, led: int) -> PelcoDCommand:
        """
        Causes an auxiliary function in the camera unit to be deactivated (LED)
        """

        validate_uint8(led)

        return self._extended(
            opcode=D_EC_CLEAR_AUX,
            sub_opcode=D_ECS_CLEAR_AUX_LED,
            data=led,
        )

    def dummy(self) -> PelcoDCommand:
        """
        This command is decoded and a general response is sent except for the
        ExSite that gives no response at all. Nothing else occurs by any Pelco
        equipment.
        """

        return self._extended(D_EC_DUMMY_1)

    def remote_reset(self) -> PelcoDCommand:
        """
        This command resets the system. It will take several seconds before the
        system is ready to resume normal operation. This is the same as turning
        the system off and then back on.
        """

        return self._extended(D_EC_RESET)

    def set_zone_start(self, zone_id: int) -> PelcoDCommand:
        validate_zone_id(zone_id)

        return self._extended(D_EC_ZONE_START, data=zone_id)

    def set_zone_end(self, zone_id: int) -> PelcoDCommand:
        validate_zone_id(zone_id)

        return self._extended(D_EC_ZONE_END, data=zone_id)

    def write_character_to_screen(
        self, screen_column: int, ascii_char: int
    ) -> PelcoDCommand:
        validate_screen_column(screen_column)
        validate_uint8(ascii_char)

        return self._command(
            command_2=D_EC_WRITE_CHAR,
            data_1=screen_column,
            data_2=ascii_char,
        )

    def zone_scan_on(self) -> PelcoDCommand:
        return self._extended(D_EC_ZONE_ON)

    def zone_scan_off(self) -> PelcoDCommand:
        return self._extended(D_EC_ZONE_OFF)

    def set_pattern_start(self, pattern_id: int) -> PelcoDCommand:
        validate_pattern_id(pattern_id)

        return self._extended(D_EC_START_RECORD, data=pattern_id)

    def set_pattern_end(self, pattern_id: int) -> PelcoDCommand:
        validate_pattern_id(pattern_id)

        return self._extended(D_EC_END_RECORD, data=pattern_id)

    def run_pattern(self, pattern_id: int) -> PelcoDCommand:
        validate_pattern_id(pattern_id)

        return self._extended(D_EC_START_PLAY, data=pattern_id)

    def set_zoom_speed(self, zoom_speed: int) -> PelcoDCommand:
        validate_zoom_speed(zoom_speed)

        return self._extended(D_EC_ZOOM_SPEED, data=zoom_speed)

    def set_focus_speed(self, focus_speed: int) -> PelcoDCommand:
        """
        Set Focus Speed (FOCUS SPEED)
        """

        validate_focus_speed(focus_speed)

        return self._extended(D_EC_FOCUS_SPEED, data=focus_speed)

    def reset_camera_to_defaults(self) -> PelcoDCommand:
        return self._extended(D_EC_CAMERA_RESET)

    def auto_focus(self, enabled: bool = True) -> PelcoDCommand:
        """
        Auto Focus (AUTO FOCUS)

        Control whether auto focus is on (default) or off.
        """

        auto_focus_ctrl: int = (
            D_ECD_AUTO_FOCUS_AUTO if enabled else D_ECD_AUTO_FOCUS_OFF
        )

        return self._extended(D_EC_AUTO_FOCUS, data=auto_focus_ctrl)

    def auto_iris(self, enabled: bool = True) -> PelcoDCommand:
        """
        Auto Iris (AUTO IRIS)

        Control whether auto iris is on (default) or off.
        """

        auto_iris_ctrl: int = D_ECD_AUTO_IRIS_AUTO if enabled else D_ECD_AUTO_IRIS_OFF

        return self._extended(D_EC_AUTO_IRIS, data=auto_iris_ctrl)

    def agc(self, enabled: bool = False) -> PelcoDCommand:
        """
        Automatic Gain Control (AGC)

        Control whether AGC (automatic gain control) is on or off (default).
        Sending an ADJUST GAIN command turns AGC off.
        """

        agc_ctrl: int = D_ECD_AUTO_AGC_AUTO if enabled else D_ECD_AUTO_AGC_OFF

        return self._extended(D_EC_AGC, data=agc_ctrl)

    def blc(self, enabled: bool = False) -> PelcoDCommand:
        """
        Backlight Compensation (BLC)

        Control whether backlight compensation is turned on or off (default).
        """
        blc_ctrl: int = D_ECD_AUTO_BLC_ON if enabled else D_ECD_AUTO_BLC_OFF

        return self._extended(D_EC_BLC, data=blc_ctrl)

    def awb(self, enabled: bool = True) -> PelcoDCommand:
        """
        Auto White Balance (AWB)

        Control whether auto white balance is turned on (default) or off.
        Sending an ADJUST WHITE BALANCE command turns auto white balance off.
        """

        awb_ctrl: int = D_ECD_AUTO_AWB_ON if enabled else D_ECD_AUTO_AWB_OFF

        return self._extended(D_EC_AWB, data=awb_ctrl)

    def device_phase(self) -> PelcoDCommand:
        """
        Enable Device Phase Delay Mode (DEVICE PHASE)

        When device phase delay is set, the phase delay is set by the device
        (there may be a manual adjustment). Sending an ADJUST LINE LOCK phase
        delay command will disable device phase delay mode.
        """

        return self._extended(D_EC_DEVICE_PHASE)

    def set_shutter_speed(self, shutter_speed: int) -> PelcoDCommand:
        validate_shutter_speed(shutter_speed)

        return self._extended(D_EC_SHUTTER_SPEED, data=shutter_speed)

    def adjust_line_lock_phase_delay_new(
        self, line_lock_phase_delay: int
    ) -> PelcoDCommand:
        validate_line_lock_phase_delay(line_lock_phase_delay)

        return self._extended(
            opcode=D_EC_ADJUST_PHASE,
            sub_opcode=D_ECS_ADJUST_PHASE_NEW,
            data=line_lock_phase_delay,
        )

    def adjust_line_lock_phase_delay_delta(
        self, line_lock_phase_delay: int
    ) -> PelcoDCommand:
        validate_line_lock_phase_delay(line_lock_phase_delay)

        return self._extended(
            opcode=D_EC_ADJUST_PHASE,
            sub_opcode=D_ECS_ADJUST_PHASE_DELTA,
            data=line_lock_phase_delay,
        )

    def adjust_white_balance_rb_new(self, white_balance: int) -> PelcoDCommand:
        validate_white_balance_rb(white_balance)

        return self._extended(
            opcode=D_EC_ADJUST_RB_WB,
            sub_opcode=D_ECS_ADJUST_RB_WB_NEW,
            data=white_balance,
        )

    def adjust_white_balance_rb_delta(self, white_balance: int) -> PelcoDCommand:
        validate_white_balance_rb(white_balance)

        return self._extended(
            opcode=D_EC_ADJUST_RB_WB,
            sub_opcode=D_ECS_ADJUST_RB_WB_DELTA,
            data=white_balance,
        )

    def adjust_white_balance_mg_new(self, white_balance: int) -> PelcoDCommand:
        validate_white_balance_mg(white_balance)

        return self._extended(
            opcode=D_EC_ADJUST_MG_WB,
            sub_opcode=D_ECS_ADJUST_MG_WB_NEW,
            data=white_balance,
        )

    def adjust_white_balance_mg_delta(self, white_balance: int) -> PelcoDCommand:
        validate_white_balance_mg(white_balance)

        return self._extended(
            opcode=D_EC_ADJUST_MG_WB,
            sub_opcode=D_ECS_ADJUST_MG_WB_DELTA,
            data=white_balance,
        )

    def adjust_gain(self, adjust_gain_mode: int, adjust_gain: int) -> PelcoDCommand:
        assert MIN_ADJUST_GAIN_MODE <= adjust_gain_mode <= MAX_ADJUST_GAIN_MODE
        assert MIN_ADJUST_GAIN <= adjust_gain <= MAX_ADJUST_GAIN

        adjust_gain_msb: int = (adjust_gain >> UINT8_SIZE) & UINT8_MAX
        adjust_gain_lsb: int = adjust_gain & UINT8_MAX

        return self._command(
            command_1=adjust_gain_mode,
            command_2=D_EC_ADJUST_GAIN,
            data_1=adjust_gain_msb,
            data_2=adjust_gain_lsb,
        )

    def adjust_auto_iris_level(
        self, auto_iris_level_mode: int, auto_iris_level: int
    ) -> PelcoDCommand:
        assert (
            MIN_ADJUST_AUTO_IRIS_LEVEL_MODE
            <= auto_iris_level_mode
            <= MAX_ADJUST_AUTO_IRIS_LEVEL_MODE
        )
        assert (
            MIN_ADJUST_AUTO_IRIS_LEVEL <= auto_iris_level <= MAX_ADJUST_AUTO_IRIS_LEVEL
        )

        auto_iris_level_msb: int = (auto_iris_level >> UINT8_SIZE) & UINT8_MAX
        auto_iris_level_lsb: int = auto_iris_level & UINT8_MAX

        return self._command(
            command_1=auto_iris_level_mode,
            command_2=D_EC_ADJUST_AI_LEVEL,
            data_1=auto_iris_level_msb,
            data_2=auto_iris_level_lsb,
        )

    def adjust_auto_iris_peak_value(
        self, auto_iris_peak_value_mode: int, auto_iris_peak_value: int
    ) -> PelcoDCommand:
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

        auto_iris_peak_value_msb: int = (auto_iris_peak_value >> UINT8_SIZE) & UINT8_MAX
        auto_iris_peak_value_lsb: int = auto_iris_peak_value & UINT8_MAX

        return self._command(
            command_1=auto_iris_peak_value_mode,
            command_2=D_EC_ADJUST_AI_PEAK,
            data_1=auto_iris_peak_value_msb,
            data_2=auto_iris_peak_value_lsb,
        )

    def query(self, query_type: int) -> PelcoDCommand:
        assert MIN_QUERY_TYPE <= query_type <= MAX_QUERY_TYPE

        # This command does not utilise the address field.
        # This is so that the address of a unit may be determined programatically.
        return PelcoDCommand(
            # address=self.address,
            command_1=query_type,
            command_2=D_EC_QUERY,
        )

    # TODO: preset_scan

    def set_zero_position(self) -> PelcoDCommand:
        return self._command(
            command_2=D_EC_SET_ZERO,
        )

    def set_pan_position(self, pan_position: int) -> PelcoDCommand:
        assert MIN_PAN_POSITION <= pan_position <= MAX_PAN_POSITION

        pan_msb: int = (pan_position >> UINT8_SIZE) & UINT8_MAX
        pan_lsb: int = pan_position & UINT8_MAX

        return self._command(
            command_2=D_EC_SET_PAN,
            data_1=pan_msb,
            data_2=pan_lsb,
        )

    def set_tilt_position(self, tilt_position: int) -> PelcoDCommand:
        assert MIN_TILT_POSITION <= tilt_position <= MAX_TILT_POSITION

        tilt_msb: int = (tilt_position >> UINT8_SIZE) & UINT8_MAX
        tilt_lsb: int = tilt_position & UINT8_MAX

        return self._command(
            command_2=D_EC_SET_TILT,
            data_1=tilt_msb,
            data_2=tilt_lsb,
        )

    def set_zoom_position(self, zoom_position: int) -> PelcoDCommand:
        assert MIN_ZOOM_POSITION <= zoom_position <= MAX_ZOOM_POSITION

        zoom_msb: int = (zoom_position >> UINT8_SIZE) & UINT8_MAX
        zoom_lsb: int = zoom_position & UINT8_MAX

        return self._command(
            command_2=D_EC_ZOOM,
            data_1=zoom_msb,
            data_2=zoom_lsb,
        )

    def query_pan_position(self) -> PelcoDCommand:
        return self._command(
            command_2=D_EC_QUERY_PAN,
        )

    def query_tilt_position(self) -> PelcoDCommand:
        return self._command(
            command_2=D_EC_QUERY_TILT,
        )

    def query_zoom_position(self) -> PelcoDCommand:
        return self._command(
            command_2=D_EC_QUERY_ZOOM,
        )

    # TODO: prepare_for_download
    # TODO: set_magnification

    def query_magnification(self) -> PelcoDCommand:
        return PelcoDCommand(
            address=self.address,
            command_2=D_EC_QUERY_MAG,
        )

    # TODO: activate_echo_mode
    # TODO: set_remote_baud_rate
    # TODO: start_download

    def query_device_type(self) -> PelcoDCommand:
        return self._command(
            command_2=D_EC_QUERY_DEV_TYPE,
        )

    def query_diagnostic_information(self) -> PelcoDCommand:
        return self._command(
            command_2=D_EC_QUERY_DIAG_INFO,
        )

    def version_information_macro(self, command: int) -> PelcoDCommand:
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
    ) -> PelcoDCommand:
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
