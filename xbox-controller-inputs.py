from enum import Enum

import inputs
import serial.tools.list_ports
from pelco.d.master import PelcoD


class StrEnum(str, Enum):
    pass


class Button(StrEnum):
    A: str = "BTN_SOUTH"
    B: str = "BTN_EAST"
    X: str = "BTN_NORTH"
    Y: str = "BTN_WEST"
    LEFT_BUMPER: str = "BTN_TL"
    RIGHT_BUMPER: str = "BTN_TR"
    VIEW: str = "BTN_SELECT"
    MENU: str = "BTN_START"
    HOME: str = "BTN_MODE"
    LEFT_STICK: str = "BTN_THUMBL"
    RIGHT_STICK: str = "BTN_THUMBR"


class Axis(StrEnum):
    D_PAD_X: str = "ABS_HAT0X"
    D_PAD_Y: str = "ABS_HAT0Y"
    LEFT_STICK_X: str = "ABS_X"
    LEFT_STICK_Y: str = "ABS_Y"
    LEFT_TRIGGER: str = "ABS_Z"
    RIGHT_STICK_X: str = "ABS_RX"
    RIGHT_STICK_Y: str = "ABS_RY"
    RIGHT_TRIGGER: str = "ABS_RZ"


# SPEED_MAX: int = 2**6
SPEED_MAX: int = 0xF
TRIGGER_MAX: int = 2**10
STICK_MAX: int = 2**15
STICK_THRESHOLD: float = 0.1 # ignore the first 10%


def get_xbox_controller():
    for device in inputs.devices:
        if device.name == "Microsoft X-Box One S pad":
            return device

    raise Exception("Failed to find XBox Controller")


def get_serial_device() -> str:
    comports = serial.tools.list_ports.comports()

    for comport in comports:
        if comport.product == "FT232R USB UART":
            return comport.device

    raise Exception("Failed to find serial device")


camera = PelcoD(
    address=0x02,
    port=get_serial_device(),
)

xbox_controller = get_xbox_controller()

DEFAULT_SPEED: int = 0x10

def stick_value_to_speed(stick_value: int, /) -> int:
    normalised_value: float = stick_value / STICK_MAX

    if abs(normalised_value) <= STICK_THRESHOLD:
        normalised_value = 0
    else:
        if normalised_value > 0:
            normalised_value = (normalised_value-STICK_THRESHOLD)/(1-STICK_THRESHOLD)
        else:
            normalised_value = (normalised_value+STICK_THRESHOLD)/(1-STICK_THRESHOLD)

    return round(normalised_value * SPEED_MAX)

while True:
    for event in xbox_controller.read():
        # Button Up/Down Event
        if event.ev_type == "Key":
            button: Button = Button(event.code)
            down: bool = bool(event.state)

            if down:
                print(f"Button Down: {button.name}")
            else:
                print(f"Button Up: {button.name}")

                if button is Button.MENU:
                    camera.set_preset(95)

        # Hat/Axis Motion Event
        elif event.ev_type == "Absolute":
            axis: Axis = Axis(event.code)

            if axis in (Axis.D_PAD_X, Axis.D_PAD_Y):
                print(f"Hat Motion: {axis.name} -> {event.state}")

                if axis is Axis.D_PAD_X:
                    if event.state == -1:
                        print("Panning Left")
                        camera.pan_left(DEFAULT_SPEED)
                    elif event.state == 1:
                        print("Panning Right")
                        camera.pan_right(DEFAULT_SPEED)
                    else:
                        print("Stopping Panning")
                        camera.stop()
                elif axis is Axis.D_PAD_Y:
                    if event.state == -1:
                        print("Tilting Up")
                        camera.tilt_up(DEFAULT_SPEED)
                    elif event.state == 1:
                        print("Tilting Down")
                        camera.tilt_down(DEFAULT_SPEED)
                    else:
                        print("Stopping Tilting")
                        camera.stop()
            else:
                # print(f"Axis Motion: {axis.name} -> {event.state}")

                if axis is Axis.LEFT_STICK_X:
                    speed: int = stick_value_to_speed(event.state)

                    if speed > 0:
                        print(f"Panning Right (speed={speed})")
                        camera.pan_right(speed)
                    elif speed < 0:
                        print(f"Panning Left (speed={abs(speed)})")
                        camera.pan_left(abs(speed))
                    else:
                        print("Stopping Panning")
                        camera.stop()
                elif axis is Axis.RIGHT_STICK_Y:
                    speed: int = stick_value_to_speed(event.state)

                    if speed > 0:
                        print(f"Tilting Down (speed={speed})")
                        camera.tilt_down(speed)
                    elif speed < 0:
                        print(f"Tilting Up (speed={abs(speed)})")
                        camera.tilt_up(abs(speed))
                    else:
                        print("Stopping Tilting")
                        camera.stop()