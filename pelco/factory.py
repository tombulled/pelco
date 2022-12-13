from dataclasses import dataclass

from .constants import *
from .models import SendCommandModel


@dataclass
class SendCommandFactory:
    address: int

    def __init__(self, address: int = DEFAULT_ADDRESS):
        assert MIN_ADDRESS <= address <= MAX_ADDRESS

        self.address = address

    def camera_on(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=SENSE | CAMERA,
        )

    def camera_off(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=CAMERA,
        )

    def scan_auto(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=SENSE | SCAN,
        )

    def scan_manual(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=SCAN,
        )

    def iris_close(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=IRIS_CLOSE,
        )

    def iris_open(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=IRIS_OPEN,
        )

    def stop(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
        )

    def pan_right(self, speed: int) -> SendCommandModel:
        assert MIN_PAN_SPEED <= speed <= MAX_PAN_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=RIGHT,
            data_1=speed,
        )

    def pan_left(self, speed: int) -> SendCommandModel:
        assert MIN_PAN_SPEED <= speed <= MAX_PAN_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=LEFT,
            data_1=speed,
        )

    def tilt_up(self, speed: int) -> SendCommandModel:
        assert MIN_TILT_SPEED <= speed <= MAX_TILT_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=UP,
            data_2=speed,
        )

    def tilt_down(self, speed: int) -> SendCommandModel:
        assert MIN_TILT_SPEED <= speed <= MAX_TILT_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=DOWN,
            data_2=speed,
        )

    def zoom_tele(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=ZOOM_TELE,
        )

    def zoom_wide(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=ZOOM_WIDE,
        )

    def focus_far(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=FOCUS_FAR,
        )

    def focus_near(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=FOCUS_NEAR,
        )

    def set_preset(self, preset_id: int) -> SendCommandModel:
        """
        Command 0x03, Set Preset

        * This command generates a "General Reply".
        * Command Names as used by the Spectra IV software:
            * 0x0003 SET_PRESET
        * This command is used by the Endura/Atlas projects.
        * This command is used and decoded on the: ERD97P21, Esprit 3012, Intercept and LRD.
        * The defined presets may be determined by using QUERY DEFINED PRESETS and its reply of
          QUERY DEFINED PRESETS RESPONSE.

        Presets can be moved to, set, or cleared.
        
        When a move to preset command is received, the preset position stored for the preset number specified
        in the command is checked. If the position is not valid, the command is ignored. Otherwise the unit moves
        to the preset pan, tilt, zoom, and focus positions. Once the preset has been reached, the preset label is
        displayed on the second video line or where it has been moved through use of the SET 95 menu system.
        
        If any command which causes motion is received during a move to preset, the move will be aborted and
        the new command will start. These commands are: a motion command, or another move to preset command,
        Also if the move is not completed within a timeout period, the move is aborted and motion is stopped.
        
        When a SET PRESET command is received, the current pan, tilt, focus, and zoom positions are saved for
        the preset number specified in the command and the label for that preset becomes whatever is currently on
        the second video line.
        
        Usually this command will cause the camera system to remember where it is currently pointing. Other
        times it will cause a specific action to occur. The most common of specific action is a menu call command
        with either SET PRESET 95 (or SET PRESET 28 in 32 preset mode).
        
        Pre-assigned presets may not be used for position setting. If an attempt to do so is done, then the
        command is ignored with a General Reply being returned.
        
            1. DATA2 This is the preset number. The range of this value is: 0x01 -> 0xFF, 1 -> 255. Different
        camera systems have differing number of preset numbers. Preset 0 is invalid.
        
        Spectra III and ExSite saves in addition to the pan/tilt/zoom information for a preset through use of the
        menu system all items in the appropriate “preset camera setting screens”. A total of ten (10) presets may
        have this special capability. With the Spectra IV this capability has been increased to all available presets.
        
        When the unit has a password enabled, this command will cause the unit to display the password request
        screen and not proceed until a correct password is entered. There is no way to enter a password directly via
        DProtocol.
        """

        assert MIN_PRESET_ID <= preset_id <= MAX_PRESET_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_SET_PRESET,
            data_2=preset_id,
        )

    def clear_preset(self, preset_id: int) -> SendCommandModel:
        """
        Clear Preset (D_EC_CLEAR_PRESET)

        Clears the requested preset's information from the camera system.
        Pre-assigned presets may not be cleared.
        It is not necessary to clear a preset before setting it.
        """

        assert MIN_PRESET_ID <= preset_id <= MAX_PRESET_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_CLEAR_PRESET,
            data_2=preset_id,
        )

    def go_to_preset(self, preset_id: int) -> SendCommandModel:
        """
        Call Preset (D_EC_MOVE_PRESET)

        Causes the camera unit to move, at preset speed, to the requested position.
        """

        assert MIN_PRESET_ID <= preset_id <= MAX_PRESET_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_MOVE_PRESET,
            data_2=preset_id,
        )

    def flip_180_about(self) -> SendCommandModel:
        return self.go_to_preset(PRESET_FLIP)

    def go_to_zero_pan(self) -> SendCommandModel:
        return self.go_to_preset(PRESET_ZERO)

    def set_auxiliary_relay(self, aux_id: int) -> SendCommandModel:
        assert MIN_AUX_ID <= aux_id <= MAX_AUX_ID

        return SendCommandModel(
            address=self.address,
            command_1=D_ECS_SET_AUX_RELAY,
            command_2=D_EC_SET_AUX,
            data_2=aux_id,
        )

    def set_auxiliary_led(self, led: int, rate: int) -> SendCommandModel:
        assert BYTE_MIN <= led <= BYTE_MAX
        assert BYTE_MIN <= rate <= BYTE_MAX

        return SendCommandModel(
            address=self.address,
            command_1=D_ECS_SET_AUX_LED,
            command_2=D_EC_SET_AUX,
            data_1=rate,
            data_2=led,
        )

    def clear_auxiliary(self, aux_id: int) -> SendCommandModel:
        assert MIN_AUX_ID <= aux_id <= MAX_AUX_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_CLEAR_AUX,
            data_2=aux_id,
        )

    def dummy(self):
        """
        Dummy (D_EC_DUMMY_1)
        """

        ...

    def remote_reset(self) -> SendCommandModel:
        """
        Remote Reset (D_EC_RESET)

        This command resets the system. It will take several seconds before the
        system is ready to resume normal operation. This is the same as turning
        the system off and then back on.
        """

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_RESET,
        )

    def set_zone_start(self, zone_id: int) -> SendCommandModel:
        """
        Set Zone Start (D_EC_ZONE_START)
        """

        assert MIN_ZONE_ID <= zone_id <= MAX_ZONE_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_ZONE_START,
            data_2=zone_id,
        )

    def set_zone_end(self, zone_id: int) -> SendCommandModel:
        """
        Set Zone End (D_EC_ZONE_END)
        """

        assert MIN_ZONE_ID <= zone_id <= MAX_ZONE_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_ZONE_END,
            data_2=zone_id,
        )

    def write_character_to_screen(
        self, screen_column: int, ascii_char: int
    ) -> SendCommandModel:
        """
        Write Character To Screen (D_EC_WRITE_CHAR)
        """

        assert MIN_SCREEN_COLUMN <= screen_column <= MAX_SCREEN_COLUMN
        assert 0x00 <= ascii_char <= 0xFF

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_WRITE_CHAR,
            data_1=screen_column,
            data_2=ascii_char,
        )

    def zone_scan_on(self) -> SendCommandModel:
        """
        Zone Scan On (D_EC_ZONE_ON)
        """

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_ZONE_ON,
        )

    def zone_scan_off(self) -> SendCommandModel:
        """
        Zone Scan Off (D_EC_ZONE_OFF)
        """

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_ZONE_OFF,
        )

    def set_pattern_start(self, pattern_id: int) -> SendCommandModel:
        """
        Set Pattern Start (D_EC_START_RECORD)
        """

        assert MIN_PATTERN_ID <= pattern_id <= MAX_PATTERN_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_START_RECORD,
            data_2=pattern_id,
        )

    def set_pattern_end(self, pattern_id: int) -> SendCommandModel:
        """
        Set Pattern End (D_EC_END_RECORD)
        """

        assert MIN_PATTERN_ID <= pattern_id <= MAX_PATTERN_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_END_RECORD,
            data_2=pattern_id,
        )

    def run_pattern(self, pattern_id: int) -> SendCommandModel:
        """
        Run Pattern (D_EC_START_PLAY)
        """

        assert MIN_PATTERN_ID <= pattern_id <= MAX_PATTERN_ID

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_START_PLAY,
            data_2=pattern_id,
        )

    def set_zoom_speed(self, zoom_speed: int) -> SendCommandModel:
        """
        Set Zoom Speed (D_EC_ZOOM_SPEED)
        """

        assert MIN_ZOOM_SPEED <= zoom_speed <= MAX_ZOOM_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_ZOOM_SPEED,
            data_2=zoom_speed,
        )

    def set_focus_speed(self, focus_speed: int) -> SendCommandModel:
        """
        Set Focus Speed (D_EC_FOCUS_SPEED)
        """

        assert MIN_FOCUS_SPEED <= focus_speed <= MAX_FOCUS_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_FOCUS_SPEED,
            data_2=focus_speed,
        )

    def reset_camera_to_defaults(self) -> SendCommandModel:
        """
        Reset Camera to Defaults (D_EC_CAMERA_RESET)
        """

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_CAMERA_RESET,
        )

    def set_auto_focus_mode(self, auto_focus_mode: int) -> SendCommandModel:
        """
        Auto Focus (D_EC_AUTO_FOCUS)
        """

        assert MIN_AUTO_FOCUS_MODE <= auto_focus_mode <= MAX_AUTO_FOCUS_MODE

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_AUTO_FOCUS,
            data_2=auto_focus_mode,
        )

    def set_auto_iris_mode(self, auto_iris_mode: int) -> SendCommandModel:
        """
        Auto Iris (D_EC_AUTO_IRIS)
        """

        assert MIN_AUTO_IRIS_MODE <= auto_iris_mode <= MAX_AUTO_IRIS_MODE

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_AUTO_IRIS,
            data_2=auto_iris_mode,
        )

    def set_agc_mode(self, agc_mode: int) -> SendCommandModel:
        """
        AGC (D_EC_AGC)
        """

        assert MIN_AGC_MODE <= agc_mode <= MAX_AGC_MODE

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_AGC,
            data_2=agc_mode,
        )

    def set_backlight_compensation_mode(
        self, backlight_compensation_mode: int
    ) -> SendCommandModel:
        """
        Backlight Compensation (D_EC_BLC)
        """

        assert (
            MIN_BACKLIGHT_COMPENSATION_MODE
            <= backlight_compensation_mode
            <= MAX_BACKLIGHT_COMPENSATION_MODE
        )

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_BLC,
            data_2=backlight_compensation_mode,
        )

    def set_auto_white_balance_mode(
        self, auto_white_balance_mode: int
    ) -> SendCommandModel:
        """
        Auto White Balance (D_EC_AWB)
        """

        assert (
            MIN_AUTO_WHITE_BALANCE_MODE
            <= auto_white_balance_mode
            <= MAX_AUTO_WHITE_BALANCE_MODE
        )

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_AWB,
            data_2=auto_white_balance_mode,
        )

    def enable_device_phase_delay_mode(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_DEVICE_PHASE,
        )

    def set_shutter_speed(self, shutter_speed: int) -> SendCommandModel:
        assert MIN_SHUTTER_SPEED <= shutter_speed <= MAX_SHUTTER_SPEED

        shutter_speed_msb: int = (shutter_speed >> BYTE_SIZE) & BYTE_MAX
        shutter_speed_lsb: int = shutter_speed & BYTE_MAX

        return SendCommandModel(
            address=self.address,
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

        return SendCommandModel(
            address=self.address,
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

        return SendCommandModel(
            address=self.address,
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

        return SendCommandModel(
            address=self.address,
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

        return SendCommandModel(
            address=self.address,
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

        return SendCommandModel(
            address=self.address,
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

        return SendCommandModel(
            address=self.address,
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
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_SET_ZERO,
        )

    def set_pan_position(self, pan_position: int) -> SendCommandModel:
        assert MIN_PAN_POSITION <= pan_position <= MAX_PAN_POSITION

        pan_msb: int = (pan_position >> BYTE_SIZE) & BYTE_MAX
        pan_lsb: int = pan_position & BYTE_MAX

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_SET_PAN,
            data_1=pan_msb,
            data_2=pan_lsb,
        )

    def set_tilt_position(self, tilt_position: int) -> SendCommandModel:
        assert MIN_TILT_POSITION <= tilt_position <= MAX_TILT_POSITION

        tilt_msb: int = (tilt_position >> BYTE_SIZE) & BYTE_MAX
        tilt_lsb: int = tilt_position & BYTE_MAX

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_SET_TILT,
            data_1=tilt_msb,
            data_2=tilt_lsb,
        )

    def set_zoom_position(self, zoom_position: int) -> SendCommandModel:
        assert MIN_ZOOM_POSITION <= zoom_position <= MAX_ZOOM_POSITION

        zoom_msb: int = (zoom_position >> BYTE_SIZE) & BYTE_MAX
        zoom_lsb: int = zoom_position & BYTE_MAX

        return SendCommandModel(
            address=self.address,
            command_2=D_EC_ZOOM,
            data_1=zoom_msb,
            data_2=zoom_lsb,
        )

    def query_pan_position(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_QUERY_PAN,
        )

    def query_tilt_position(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_QUERY_TILT,
        )

    def query_zoom_position(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
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
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_QUERY_DEV_TYPE,
        )

    def query_diagnostic_information(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=D_EC_QUERY_DIAG_INFO,
        )

    def version_information_macro(self, command: int) -> SendCommandModel:
        assert command in list(range(MIN_VERSION_INFORMATION_MACRO_SUB_OPCODE, MAX_VERSION_INFORMATION_MACRO_SUB_OPCODE + 1, 2))

        return SendCommandModel(
            address=self.address,
            command_1=command,
            command_2=D_EC_VERSION_INFO,
        )

    def everest_macro(self, command: int, *, data_1: int = 0x00, data_2: int = 0x00) -> SendCommandModel:
        assert command in list(range(MIN_EVEREST_MACRO_SUB_OPCODE, MAX_EVEREST_MACRO_SUB_OPCODE + 1, 2))

        return SendCommandModel(
            address=self.address,
            command_1=command,
            command_2=D_EC_EVEREST,
            data_1=data_1,
            data_2=data_2,
        )

    # TODO: time_commands
    # TODO: screen_move