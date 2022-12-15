from serial import Serial

from .constants import *
from .enums import (
    FocusSpeed,
    PanSpeed,
    TiltSpeed,
    VersionInformationCommand,
    VersionInformationResponse,
    ZoomSpeed,
)
from .errors import ResponseError
from .factory import CommandFactory
from .models import ExtendedResponse, GeneralResponse, SendCommandModel


class PelcoD:
    address: int
    factory: CommandFactory
    conn: Serial

    def __init__(
        self,
        *,
        address: int = DEFAULT_ADDRESS,
        port: str = "/dev/ttyUSB0",
        baudrate: int = 2400,
        timeout: int = 1,
    ) -> None:
        self.address = address
        self.factory = CommandFactory(address=address)
        self.conn = Serial(port=port, baudrate=baudrate, timeout=timeout)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(address={self.address})"

    def send(self, command: SendCommandModel, /) -> None:
        self.conn.write(command.serialise())

    def read(self, size: int = 1, /) -> bytes:
        response: bytes = self.conn.read(size)

        if not response:
            raise ResponseError("Timed out before receiving a response")

        return response

    def send_command_general_response(
        self, command: SendCommandModel, /
    ) -> GeneralResponse:
        self.send(command)

        return GeneralResponse.deserialise(self.read(D_EC_GENERAL_REPLY_LENGTH))

    def send_command_extended_response(
        self, command: SendCommandModel, *, expected_response_opcode: int
    ) -> ExtendedResponse:
        self.send(command)

        response: ExtendedResponse = ExtendedResponse.deserialise(
            self.read(D_EC_EXTENDED_REPLY_LENGTH)
        )

        assert response.response_2 == expected_response_opcode

        return response

    def camera_on(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.camera_on())

    def camera_off(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.camera_off())

    def camera(self, on: bool) -> GeneralResponse:
        if on:
            return self.camera_on()
        else:
            return self.camera_off()

    def scan_auto(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.scan_auto())

    def scan_manual(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.scan_manual())

    def scan(self, auto: bool) -> GeneralResponse:
        if auto:
            return self.scan_auto()
        else:
            return self.scan_manual()

    def iris_close(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.iris_close())

    def iris_open(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.iris_open())

    def stop(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.stop())

    def pan_right(self, speed: int = PanSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command_general_response(self.factory.pan_right(speed))

    def pan_left(self, speed: int = PanSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command_general_response(self.factory.pan_left(speed))

    def pan(self, speed: int) -> GeneralResponse:
        if speed > 0:
            return self.pan_right(speed=speed)
        elif speed < 0:
            return self.pan_left(speed=-speed)
        else:
            return self.stop()

    def tilt_up(self, speed: int = TiltSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command_general_response(self.factory.tilt_up(speed))

    def tilt_down(self, speed: int = TiltSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command_general_response(self.factory.tilt_down(speed))

    def tilt(self, speed: int) -> GeneralResponse:
        if speed > 0:
            return self.tilt_up(speed=speed)
        elif speed < 0:
            return self.tilt_down(speed=-speed)
        else:
            return self.stop()

    def zoom_tele(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.zoom_tele())

    def zoom_wide(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.zoom_wide())

    def zoom(self, tele: bool = True) -> GeneralResponse:
        if tele:
            return self.zoom_tele()
        else:
            return self.zoom_wide()

    def focus_far(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.focus_far())

    def focus_near(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.focus_near())

    def focus(self, near: bool = True) -> GeneralResponse:
        if near:
            return self.focus_near()
        else:
            return self.focus_far()

    def set_preset(self, id: int = 0x01) -> GeneralResponse:
        return self.send_command_general_response(self.factory.set_preset(id))

    def clear_preset(self, id: int = 0x01) -> GeneralResponse:
        return self.send_command_general_response(self.factory.clear_preset(id))

    def go_to_preset(self, id: int = 0x01) -> GeneralResponse:
        return self.send_command_general_response(self.factory.go_to_preset(id))

    def flip_180_about(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.flip_180_about())

    def go_to_zero_pan(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.go_to_zero_pan())

    def set_auxiliary_relay(self, aux_id: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_auxiliary_relay(aux_id)
        )

    def set_auxiliary_led(self, led: int, rate: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_auxiliary_led(led, rate)
        )

    def clear_auxiliary(self, aux_id: int) -> GeneralResponse:
        return self.send_command_general_response(self.factory.clear_auxiliary(aux_id))

    def dummy(self) -> GeneralResponse:
        ...

    def remote_reset(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.remote_reset())

    def set_zone_start(self, zone_id: int) -> GeneralResponse:
        return self.send_command_general_response(self.factory.set_zone_start(zone_id))

    def set_zone_end(self, zone_id: int) -> GeneralResponse:
        return self.send_command_general_response(self.factory.set_zone_end(zone_id))

    def write_character_to_screen(
        self, screen_column: int, ascii_char: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.write_character_to_screen(screen_column, ascii_char)
        )

    # TODO: clear_screen
    # TODO: alarm_acknowledge

    def zone_scan_on(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.zone_scan_on())

    def zone_scan_off(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.zone_scan_off())

    def set_pattern_start(self, pattern_id: int = 0x01) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_pattern_start(pattern_id)
        )

    def set_pattern_end(self, pattern_id: int = 0x01) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_pattern_end(pattern_id)
        )

    def run_pattern(self, pattern_id: int = 0x01) -> GeneralResponse:
        return self.send_command_general_response(self.factory.run_pattern(pattern_id))

    def set_zoom_speed(self, zoom_speed: int = ZoomSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_zoom_speed(zoom_speed)
        )

    def set_focus_speed(self, focus_speed: int = FocusSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_focus_speed(focus_speed)
        )

    def reset_camera_to_defaults(self) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.reset_camera_to_defaults()
        )

    def set_auto_focus_mode(self, auto_focus_mode: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_auto_focus_mode(auto_focus_mode)
        )

    def set_auto_iris_mode(self, auto_iris_mode: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_auto_iris_mode(auto_iris_mode)
        )

    def set_agc_mode(self, agc_mode: int) -> GeneralResponse:
        return self.send_command_general_response(self.factory.set_agc_mode(agc_mode))

    def set_backlight_compensation_mode(
        self, backlight_compensation_mode: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_backlight_compensation_mode(backlight_compensation_mode)
        )

    def set_auto_white_balance_mode(
        self, auto_white_balance_mode: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_auto_white_balance_mode(auto_white_balance_mode)
        )

    def enable_device_phase_delay_mode(self) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.enable_device_phase_delay_mode()
        )

    def set_shutter_speed(self, shutter_speed: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_shutter_speed(shutter_speed)
        )

    def adjust_line_lock_phase_delay(
        self, line_lock_phase_delay_mode: int, line_lock_phase_delay: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.adjust_line_lock_phase_delay(
                line_lock_phase_delay_mode, line_lock_phase_delay
            )
        )

    def adjust_white_balance_rb(
        self, white_balance_mode: int, white_balance: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.adjust_white_balance_rb(white_balance_mode, white_balance)
        )

    def adjust_white_balance_mg(
        self, white_balance_mode: int, white_balance: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.adjust_white_balance_mg(white_balance_mode, white_balance)
        )

    def adjust_gain(self, adjust_gain_mode: int, gain: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.adjust_gain(adjust_gain_mode, gain)
        )

    def adjust_auto_iris_level(
        self, adjust_auto_iris_level_mode: int, auto_iris_level: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.adjust_auto_iris_level(
                adjust_auto_iris_level_mode, auto_iris_level
            )
        )

    def adjust_auto_iris_peak_value(
        self, adjust_auto_iris_peak_value_mode: int, auto_iris_peak_value: int
    ) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.adjust_auto_iris_peak_value(
                adjust_auto_iris_peak_value_mode, auto_iris_peak_value
            )
        )

    def query(self, query_type: int = 0x00):
        command: SendCommandModel = self.factory.query(query_type)

        self.conn.write(command.serialise())

        # NOTE: Not currently working
        # return self.s.read(18)
        raise NotImplementedError

    # TODO: preset_scan

    def set_zero_position(self) -> GeneralResponse:
        return self.send_command_general_response(self.factory.set_zero_position())

    def set_pan_position(self, pan_position: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_pan_position(pan_position)
        )

    def set_tilt_position(self, tilt_position: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_tilt_position(tilt_position)
        )

    def set_zoom_position(self, zoom_position: int) -> GeneralResponse:
        return self.send_command_general_response(
            self.factory.set_zoom_position(zoom_position)
        )

    def query_pan_position(self) -> ExtendedResponse:
        return self.send_command_extended_response(
            self.factory.query_pan_position(),
            expected_response_opcode=D_EC_PAN_RESP,
        )

    def query_tilt_position(self) -> ExtendedResponse:
        return self.send_command_extended_response(
            self.factory.query_tilt_position(),
            expected_response_opcode=D_EC_TILT_RESP,
        )

    def query_zoom_position(self) -> ExtendedResponse:
        return self.send_command_extended_response(
            self.factory.query_zoom_position(),
            expected_response_opcode=D_EC_ZOOM_RESP,
        )

    # TODO: prepare_for_download
    # TODO: set_magnification

    def query_magnification(self) -> ExtendedResponse:
        return self.send_command_extended_response(
            self.factory.query_magnification(),
            expected_response_opcode=D_EC_MAG_RESP,
        )

    # TODO: activate_echo_mode
    # TODO: set_remote_baud_rate
    # TODO: start_download

    def query_device_type(self) -> ExtendedResponse:
        return self.send_command_extended_response(
            self.factory.query_device_type(),
            expected_response_opcode=D_EC_DEV_TYPE_REP,
        )

    def query_diagnostic_information(self) -> ExtendedResponse:
        return self.send_command_extended_response(
            self.factory.query_diagnostic_information(),
            expected_response_opcode=D_EC_QUERY_DIAG_RESP,
        )

    def version_information_macro(
        self, command: int = VersionInformationCommand.SOFTWARE_VERSION_NUMBER
    ) -> ExtendedResponse:
        expected_response_opcode: int = VersionInformationResponse.for_command(
            VersionInformationCommand(command)
        )

        return self.send_command_extended_response(
            self.factory.version_information_macro(command),
            expected_response_opcode=expected_response_opcode,
        )

    def everest_macro(
        self,
        command: int,
        data_1: int = 0x00,
        data_2: int = 0x00,
    ) -> ExtendedResponse:
        # TODO: Some commands do not return a response. These need to be supported.
        expected_response_opcode: int = command + 1

        return self.send_command_extended_response(
            self.factory.everest_macro(command, data_1=data_1, data_2=data_2),
            expected_response_opcode=expected_response_opcode,
        )

    # TODO: time_commands
    # TODO: screen_move
