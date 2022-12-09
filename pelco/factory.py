from dataclasses import dataclass

from .constants import *
from .models import SendCommandModel


@dataclass
class SendCommandFactory:
    address: int

    def __init__(self, address: int = 0x01):
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

    def set_preset(self, id: int) -> SendCommandModel:
        """
        Set Preset (D_EC_SET_PRESET)
        """

        assert MIN_PRESET < id <= MAX_PRESET

        return SendCommandModel(
            address=self.address,
            command_2=SET_PRESET,
            data_2=id,
        )

    def clear_preset(self, id: int) -> SendCommandModel:
        """
        Clear Preset (D_EC_CLEAR_PRESET)

        Clears the requested preset's information from the camera system.
        Pre-assigned presets may not be cleared.
        It is not necessary to clear a preset before setting it.
        """

        assert MIN_PRESET < id <= MAX_PRESET

        return SendCommandModel(
            address=self.address,
            command_2=CLEAR_PRESET,
            data_2=id,
        )

    def go_to_preset(self, id: int) -> SendCommandModel:
        """
        Call Preset (D_EC_MOVE_PRESET)

        Causes the camera unit to move, at preset speed, to the requested position.
        """

        assert MIN_PRESET < id <= MAX_PRESET

        return SendCommandModel(
            address=self.address,
            command_2=GO_TO_PRESET,
            data_2=id,
        )

    def flip_180_about(self) -> SendCommandModel:
        return self.go_to_preset(PRESET_FLIP)

    def go_to_zero_pan(self) -> SendCommandModel:
        return self.go_to_preset(PRESET_ZERO)

    def set_auxiliary(self, aux_id: int) -> SendCommandModel:
        assert MIN_AUX_ID <= aux_id <= MAX_AUX_ID

        return SendCommandModel(
            address=self.address,
            command_2=SET_AUXILIARY,
            data_2=aux_id,
        )

    def clear_auxiliary(self, aux_id: int) -> SendCommandModel:
        assert MIN_AUX_ID <= aux_id <= MAX_AUX_ID

        return SendCommandModel(
            address=self.address,
            command_2=CLEAR_AUXILIARY,
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
            command_2=REMOTE_RESET,
        )

    def set_zone_start(self, zone_id: int) -> SendCommandModel:
        """
        Set Zone Start (D_EC_ZONE_START)
        """

        assert MIN_ZONE_ID <= zone_id <= MAX_ZONE_ID

        return SendCommandModel(
            address=self.address,
            command_2=SET_ZONE_START,
            data_2=zone_id,
        )

    def set_zone_end(self, zone_id: int) -> SendCommandModel:
        """
        Set Zone End (D_EC_ZONE_END)
        """

        assert MIN_ZONE_ID <= zone_id <= MAX_ZONE_ID

        return SendCommandModel(
            address=self.address,
            command_2=SET_ZONE_END,
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
            command_2=WRITE_CHARACTER_TO_SCREEN,
            data_1=screen_column,
            data_2=ascii_char,
        )

    def zone_scan_on(self) -> SendCommandModel:
        """
        Zone Scan On (D_EC_ZONE_ON)
        """

        return SendCommandModel(
            address=self.address,
            command_2=ZONE_SCAN_ON,
        )

    def zone_scan_off(self) -> SendCommandModel:
        """
        Zone Scan Off (D_EC_ZONE_OFF)
        """

        return SendCommandModel(
            address=self.address,
            command_2=ZONE_SCAN_OFF,
        )

    def set_pattern_start(self, pattern_id: int) -> SendCommandModel:
        """
        Set Pattern Start (D_EC_START_RECORD)
        """

        assert MIN_PATTERN_ID <= pattern_id <= MAX_PATTERN_ID

        return SendCommandModel(
            address=self.address,
            command_2=SET_PATTERN_START,
            data_2=pattern_id,
        )

    def set_pattern_end(self, pattern_id: int) -> SendCommandModel:
        """
        Set Pattern End (D_EC_END_RECORD)
        """

        assert MIN_PATTERN_ID <= pattern_id <= MAX_PATTERN_ID

        return SendCommandModel(
            address=self.address,
            command_2=SET_PATTERN_STOP,
            data_2=pattern_id,
        )

    def run_pattern(self, pattern_id: int) -> SendCommandModel:
        """
        Run Pattern (D_EC_START_PLAY)
        """

        assert MIN_PATTERN_ID <= pattern_id <= MAX_PATTERN_ID

        return SendCommandModel(
            address=self.address,
            command_2=RUN_PATTERN,
            data_2=pattern_id,
        )

    def set_zoom_speed(self, zoom_speed: int) -> SendCommandModel:
        """
        Set Zoom Speed (D_EC_ZOOM_SPEED)
        """

        assert MIN_ZOOM_SPEED <= zoom_speed <= MAX_ZOOM_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=SET_ZOOM_SPEED,
            data_2=zoom_speed,
        )

    def set_focus_speed(self, focus_speed: int) -> SendCommandModel:
        """
        Set Focus Speed (D_EC_FOCUS_SPEED)
        """

        assert MIN_FOCUS_SPEED <= focus_speed <= MAX_FOCUS_SPEED

        return SendCommandModel(
            address=self.address,
            command_2=SET_FOCUS_SPEED,
            data_2=focus_speed,
        )

    def reset_camera_to_defaults(self) -> SendCommandModel:
        """
        Reset Camera to Defaults (D_EC_CAMERA_RESET)
        """

        return SendCommandModel(
            address=self.address,
            command_2=RESET_CAMERA_DEFAULTS,
        )

    def set_auto_focus_mode(self, auto_focus_mode: int) -> SendCommandModel:
        """
        Auto Focus (D_EC_AUTO_FOCUS)
        """

        assert MIN_AUTO_FOCUS_MODE <= auto_focus_mode <= MAX_AUTO_FOCUS_MODE

        return SendCommandModel(
            address=self.address,
            command_2=AUTO_FOCUS_MODE,
        )

    def set_auto_iris_mode(self, auto_iris_mode: int) -> SendCommandModel:
        """
        Auto Iris (D_EC_AUTO_IRIS)
        """

        assert MIN_AUTO_IRIS_MODE <= auto_iris_mode <= MAX_AUTO_IRIS_MODE

        return SendCommandModel(
            address=self.address,
            command_2=AUTO_IRIS_MODE,
        )