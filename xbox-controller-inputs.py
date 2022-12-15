from typing import Callable

import serial.tools.list_ports

from pelco.d.master import PelcoD
from xboxonecontroller.discovery import find_controllers
from xboxonecontroller.enums import Axis, Button, EventType

# SPEED_MAX: int = 2**6
SPEED_MAX: int = 0xF
TRIGGER_MAX: int = 2**10
STICK_MAX: int = 2**15
STICK_THRESHOLD: float = 0.1  # Ignore the first 10%


def get_xbox_controller():
    controllers = find_controllers()

    if controllers:
        return controllers[0]
    else:
        raise Exception("Failed to find XBox Controller")


def get_serial_device() -> str:
    comports = serial.tools.list_ports.comports()

    for comport in comports:
        if comport.product == "FT232R USB UART":
            return comport.device

    raise Exception("Failed to find serial device")


# camera = PelcoD(
#     address=0x02,
#     port=get_serial_device(),
# )


class FakeCamera:
    def __getattr__(self, _: str) -> Callable[..., None]:
        return lambda *args, **kwargs: None


camera = FakeCamera()

xbox_controller = get_xbox_controller()

DEFAULT_SPEED: int = 0x10


def stick_value_to_speed(stick_value: int, /) -> int:
    normalised_value: float = stick_value / STICK_MAX

    if abs(normalised_value) <= STICK_THRESHOLD:
        normalised_value = 0
    else:
        if normalised_value > 0:
            normalised_value = (normalised_value - STICK_THRESHOLD) / (
                1 - STICK_THRESHOLD
            )
        else:
            normalised_value = (normalised_value + STICK_THRESHOLD) / (
                1 - STICK_THRESHOLD
            )

    return round(normalised_value * SPEED_MAX)


left_stick_x: int = 0
left_stick_y: int = 0
right_stick_x: int = 0
right_stick_y: int = 0
left_trigger: int = 0
right_trigger: int = 0
d_pad_x: int = 0
d_pad_y: int = 0

while True:
    for event in xbox_controller.read():
        if event.type == EventType.BUTTON:
            button: Button = event.subject
            down: bool = bool(event.value)

            if down:
                print(f"Button Down: {button.name}")

                if button is Button.RIGHT_BUMPER:
                    print("\t Starting Focus Near")
                    camera.focus_near()
                elif button is Button.LEFT_BUMPER:
                    print("\t Starting Focus Far")
                    camera.focus_far()
            else:
                print(f"Button Up: {button.name}")

                if button is Button.MENU:
                    print("\t SET PRESET 95")
                    camera.set_preset(95)
                elif button is Button.A:
                    print("\t TODO: Find purpose...")
                elif button is Button.B:  # Note: pointless as could flick a button?
                    print("\t Stopping")
                    camera.stop()
                elif button is Button.X:
                    print("\t Toggle Wiper?")  # TODO
                elif button is Button.Y:
                    print("\t TODO: Find purpose...")
                elif button is Button.RIGHT_BUMPER:
                    print("\t STOP")
                    camera.stop()
                elif button is Button.LEFT_BUMPER:
                    print("\t STOP")
                    camera.stop()
        elif event.type == EventType.AXIS:
            axis: Axis = event.subject

            if axis in (Axis.D_PAD_X, Axis.D_PAD_Y):
                print(f"Hat Motion: {axis.name} -> {event.value}")

                if axis is Axis.D_PAD_X:
                    d_pad_x = event.value
                elif axis is Axis.D_PAD_Y:
                    d_pad_y = event.value

                if d_pad_y == 0 and d_pad_x == -1:
                    print("\t Panning Left")
                    camera.pan_left(DEFAULT_SPEED)
                elif d_pad_y == 0 and d_pad_x == 1:
                    print("\t Panning Right")
                    camera.pan_right(DEFAULT_SPEED)
                elif d_pad_x == 0 and d_pad_y == -1:
                    print("\t Tilting Up")
                    camera.tilt_up(DEFAULT_SPEED)
                elif d_pad_x == 0 and d_pad_y == 1:
                    print("\t Tilting Down")
                    camera.tilt_down(DEFAULT_SPEED)
                elif d_pad_y == -1 and d_pad_x == -1:
                    print("\t Tilting Up and Panning Left (currently unsupported)")
                elif d_pad_y == -1 and d_pad_x == 1:
                    print("\t Tilting Up and Panning Right (currently unsupported)")
                elif d_pad_y == 1 and d_pad_x == -1:
                    print("\t Tilting Down and Panning Left (currently unsupported)")
                elif d_pad_y == 1 and d_pad_x == 1:
                    print("\t Tilting Down and Panning Right (currently unsupported)")
                elif d_pad_y == 0 and d_pad_x == 0:
                    print("\t Stopping Panning")
                    camera.stop()
            else:
                # print(f"Axis Motion: {axis.name} -> {event.value}")

                if axis in (Axis.LEFT_STICK_X, Axis.LEFT_STICK_Y):
                    dx: int = 0
                    dy: int = 0
                    speed_dx: int = 0
                    speed_dy: int = 0

                    if axis is Axis.LEFT_STICK_X:
                        dx = abs(abs(left_stick_x) - abs(event.value))
                        speed_dx = abs(
                            abs(stick_value_to_speed(left_stick_x))
                            - abs(stick_value_to_speed(event.value))
                        )
                        left_stick_x = event.value
                    elif axis is Axis.LEFT_STICK_Y:
                        dy = abs(abs(left_stick_y) - abs(event.value))
                        speed_dy = abs(
                            abs(stick_value_to_speed(left_stick_y))
                            - abs(stick_value_to_speed(event.value))
                        )
                        left_stick_y = event.value

                    if speed_dx == 0 and speed_dy == 0:
                        # No significant difference, ignoring
                        continue

                    speed_x: int = stick_value_to_speed(left_stick_x)
                    speed_y: int = stick_value_to_speed(left_stick_y)

                    if speed_x == 0 and speed_y == 0:
                        print("\t Stopping")
                        camera.stop()
                    elif speed_x == 0 and speed_y > 0:
                        print(f"\t Tilting Down (tilt_speed={speed_y})")
                    elif speed_x == 0 and speed_y < 0:
                        print(f"\t Tilting Up (tilt_speed={abs(speed_y)})")
                    elif speed_y == 0 and speed_x > 0:
                        print(f"\t Panning Right (pan_speed={speed_x})")
                    elif speed_y == 0 and speed_x < 0:
                        print(f"\t Panning Left (pan_speed={abs(speed_x)})")
                    elif speed_x > 0 and speed_y > 0:
                        print(
                            f"\t Tilting Down and Panning Right (tilt_speed={speed_y}, pan_speed={speed_x})"
                        )
                    elif speed_x > 0 and speed_y < 0:
                        print(
                            f"\t Tilting Up and Panning Right (tilt_speed={abs(speed_y)}, pan_speed={speed_x})"
                        )
                    elif speed_x < 0 and speed_y > 0:
                        print(
                            f"\t Tilting Down and Panning Left (tilt_speed={speed_y}, pan_speed={abs(speed_x)})"
                        )
                    elif speed_x < 0 and speed_y < 0:
                        print(
                            f"\t Tilting Up and Panning Left (tilt_speed={abs(speed_y)}, pan_speed={abs(speed_x)})"
                        )
                elif axis is Axis.LEFT_TRIGGER:
                    print("\t TODO: Zoom Out")
                elif axis is Axis.RIGHT_TRIGGER:
                    print("\t TODO: Zoom In")
