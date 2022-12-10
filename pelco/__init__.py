import serial

from .constants import *
from .enums import FocusSpeed, PanSpeed, TiltSpeed, ZoomSpeed
from .factory import SendCommandFactory
from .models import GeneralResponse, SendCommandModel


class Pelco:
    address: int

    def __init__(self, *, address: int = 0x01) -> None:
        self.address = address

        self.command_factory = SendCommandFactory(address=address)
        self.s = serial.Serial(port="/dev/ttyUSB0", baudrate=2400, timeout=1)

    def send_command(self, command: SendCommandModel, /) -> GeneralResponse:
        self.s.write(command.serialise())

        return GeneralResponse.deserialise(self.s.read(4))

    def camera_on(self) -> GeneralResponse:
        return self.send_command(self.command_factory.camera_on())

    def camera_off(self) -> GeneralResponse:
        return self.send_command(self.command_factory.camera_off())

    def camera(self, on: bool) -> GeneralResponse:
        if on:
            return self.camera_on()
        else:
            return self.camera_off()

    def scan_auto(self) -> GeneralResponse:
        return self.send_command(self.command_factory.scan_auto())

    def scan_manual(self) -> GeneralResponse:
        return self.send_command(self.command_factory.scan_manual())

    def scan(self, auto: bool) -> GeneralResponse:
        if auto:
            return self.scan_auto()
        else:
            return self.scan_manual()

    def iris_close(self) -> GeneralResponse:
        return self.send_command(self.command_factory.iris_close())

    def iris_open(self) -> GeneralResponse:
        return self.send_command(self.command_factory.iris_open())

    def stop(self) -> GeneralResponse:
        return self.send_command(self.command_factory.stop())

    def pan_right(self, speed: int = PanSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command(self.command_factory.pan_right(speed))

    def pan_left(self, speed: int = PanSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command(self.command_factory.pan_left(speed))

    def pan(self, speed: int) -> GeneralResponse:
        if speed > 0:
            return self.pan_right(speed=speed)
        elif speed < 0:
            return self.pan_left(speed=-speed)
        else:
            return self.stop()

    def tilt_up(self, speed: int = TiltSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command(self.command_factory.tilt_up(speed))

    def tilt_down(self, speed: int = TiltSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command(self.command_factory.tilt_down(speed))

    def tilt(self, speed: int) -> GeneralResponse:
        if speed > 0:
            return self.tilt_up(speed=speed)
        elif speed < 0:
            return self.tilt_down(speed=-speed)
        else:
            return self.stop()

    def zoom_tele(self) -> GeneralResponse:
        return self.send_command(self.command_factory.zoom_tele())

    def zoom_wide(self) -> GeneralResponse:
        return self.send_command(self.command_factory.zoom_wide())

    def zoom(self, tele: bool = True) -> GeneralResponse:
        if tele:
            return self.zoom_tele()
        else:
            return self.zoom_wide()

    def focus_far(self) -> GeneralResponse:
        return self.send_command(self.command_factory.focus_far())

    def focus_near(self) -> GeneralResponse:
        return self.send_command(self.command_factory.focus_near())

    def focus(self, near: bool = True) -> GeneralResponse:
        if near:
            return self.focus_near()
        else:
            return self.focus_far()

    def set_preset(self, id: int = 0x01) -> GeneralResponse:
        return self.send_command(self.command_factory.set_preset(id))

    def clear_preset(self, id: int = 0x01) -> GeneralResponse:
        return self.send_command(self.command_factory.clear_preset(id))

    def go_to_preset(self, id: int = 0x01) -> GeneralResponse:
        return self.send_command(self.command_factory.go_to_preset(id))

    def flip_180_about(self) -> GeneralResponse:
        return self.send_command(self.command_factory.flip_180_about())

    def go_to_zero_pan(self) -> GeneralResponse:
        return self.send_command(self.command_factory.go_to_zero_pan())

    def set_auxiliary(self, aux_id: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_auxiliary(aux_id))

    def clear_auxiliary(self, aux_id: int) -> GeneralResponse:
        return self.send_command(self.command_factory.clear_auxiliary(aux_id))

    def dummy(self) -> GeneralResponse:
        ...

    def remote_reset(self) -> GeneralResponse:
        return self.send_command(self.command_factory.remote_reset())

    def set_zone_start(self, zone_id: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_zone_start(zone_id))

    def set_zone_end(self, zone_id: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_zone_end(zone_id))

    def write_character_to_screen(
        self, screen_column: int, ascii_char: int
    ) -> GeneralResponse:
        return self.send_command(
            self.command_factory.write_character_to_screen(screen_column, ascii_char)
        )

    # TODO: clear_screen
    # TODO: alarm_acknowledge

    def zone_scan_on(self) -> GeneralResponse:
        return self.send_command(self.command_factory.zone_scan_on())

    def zone_scan_off(self) -> GeneralResponse:
        return self.send_command(self.command_factory.zone_scan_off())

    def set_pattern_start(self, pattern_id: int = 0x01) -> GeneralResponse:
        return self.send_command(self.command_factory.set_pattern_start(pattern_id))

    def set_pattern_end(self, pattern_id: int = 0x01) -> GeneralResponse:
        return self.send_command(self.command_factory.set_pattern_end(pattern_id))

    def run_pattern(self, pattern_id: int = 0x01) -> GeneralResponse:
        return self.send_command(self.command_factory.run_pattern(pattern_id))

    def set_zoom_speed(self, zoom_speed: int = ZoomSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command(self.command_factory.set_zoom_speed(zoom_speed))

    def set_focus_speed(self, focus_speed: int = FocusSpeed.MEDIUM) -> GeneralResponse:
        return self.send_command(self.command_factory.set_focus_speed(focus_speed))

    def reset_camera_to_defaults(self) -> GeneralResponse:
        return self.send_command(self.command_factory.reset_camera_to_defaults())

    def set_auto_focus_mode(self, auto_focus_mode: int) -> GeneralResponse:
        return self.send_command(
            self.command_factory.set_auto_focus_mode(auto_focus_mode)
        )

    def set_auto_iris_mode(self, auto_iris_mode: int) -> GeneralResponse:
        return self.send_command(
            self.command_factory.set_auto_iris_mode(auto_iris_mode)
        )

    def set_agc_mode(self, agc_mode: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_agc_mode(agc_mode))

    def set_backlight_compensation_mode(
        self, backlight_compensation_mode: int
    ) -> GeneralResponse:
        return self.send_command(
            self.command_factory.set_backlight_compensation_mode(
                backlight_compensation_mode
            )
        )

    def set_auto_white_balance_mode(
        self, auto_white_balance_mode: int
    ) -> GeneralResponse:
        return self.send_command(
            self.command_factory.set_auto_white_balance_mode(auto_white_balance_mode)
        )

    def enable_device_phase_delay_mode(self) -> GeneralResponse:
        return self.send_command(self.command_factory.enable_device_phase_delay_mode())

    def set_shutter_speed(self, shutter_speed: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_shutter_speed(shutter_speed))

    def adjust_line_lock_phase_delay(
        self, line_lock_phase_delay_mode: int, line_lock_phase_delay: int
    ) -> GeneralResponse:
        return self.send_command(
            self.command_factory.adjust_line_lock_phase_delay(
                line_lock_phase_delay_mode, line_lock_phase_delay
            )
        )

    def adjust_white_balance_rb(
        self, white_balance_mode: int, white_balance: int
    ) -> GeneralResponse:
        return self.send_command(
            self.command_factory.adjust_white_balance_rb(
                white_balance_mode, white_balance
            )
        )

    def adjust_white_balance_mg(
        self, white_balance_mode: int, white_balance: int
    ) -> GeneralResponse:
        return self.send_command(
            self.command_factory.adjust_white_balance_mg(
                white_balance_mode, white_balance
            )
        )

    # ...

    def set_zero_position(self) -> GeneralResponse:
        return self.send_command(self.command_factory.set_zero_position())

    def set_pan_position(self, pan_position: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_pan_position(pan_position))

    def set_tilt_position(self, tilt_position: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_tilt_position(tilt_position))

    def set_zoom_position(self, zoom_position: int) -> GeneralResponse:
        return self.send_command(self.command_factory.set_zoom_position(zoom_position))
