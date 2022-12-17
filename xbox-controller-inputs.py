from typing import Callable, Sequence

import serial.tools.list_ports
from loguru import logger
from pelco.d.errors import ResponseError
from pelco.d.master import PelcoD
from xboxonecontroller.discovery import find_controllers
from xboxonecontroller.enums import Axis, Button, EventType

SPEED_MAX: int = 2**6 - 1
# SPEED_MAX: int = 0xF
TRIGGER_MAX: int = 2**10
STICK_MAX: int = 2**15

PAN_SPEED_MIN: int = 0x00
PAN_SPEED_MAX: int = 0x3F
PAN_SPEED_STEP: int = 0x01

TILT_SPEED_MIN: int = 0x00
TILT_SPEED_MAX: int = 0x3F
TILT_SPEED_STEP: int = 0x01

ZOOM_SPEED_MIN: int = 0x00
ZOOM_SPEED_MAX: int = 0x03
ZOOM_SPEED_STEP: int = 0x01

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

class FakeCamera:
    def __getattr__(self, _: str) -> Callable[..., None]:
        return lambda *args, **kwargs: None


camera = PelcoD(
    address=0x02,
    port=get_serial_device(),
)
# camera = FakeCamera()

xbox_controller = get_xbox_controller()

DEFAULT_SPEED: int = 0x1F


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

def trigger_value_to_zoom_speed(value: int, /) -> int:
    zoom_speeds: Sequence[int] = tuple(range(ZOOM_SPEED_MIN, ZOOM_SPEED_MAX + 1, ZOOM_SPEED_STEP))
    max_index: int = len(zoom_speeds)-1
    normalised_value: float = value / TRIGGER_MAX
    zoom_speed_index: int = round(normalised_value * max_index)

    return zoom_speeds[zoom_speed_index]


left_stick_x: int = 0
left_stick_y: int = 0
right_stick_x: int = 0
right_stick_y: int = 0
left_trigger: int = 0
right_trigger: int = 0
d_pad_x: int = 0
d_pad_y: int = 0

while True:
    try:
        for event in xbox_controller.read():
            if event.type == EventType.BUTTON:
                button: Button = event.subject
                down: bool = bool(event.value)

                if down:
                    if button is Button.RIGHT_BUMPER:
                        logger.info("Starting Focus Near")
                        camera.focus_near()
                    elif button is Button.LEFT_BUMPER:
                        logger.info("Starting Focus Far")
                        camera.focus_far()
                else:
                    if button is Button.MENU:
                        logger.info("Opening menu")
                        camera.set_preset(95)
                    elif button is Button.VIEW:
                        logger.info("VIEW")
                    elif button is Button.A:
                        logger.info("A")
                    elif button is Button.B:  # Note: pointless as could flick a button?
                        logger.info("Stopping motion")
                        camera.stop()
                    elif button is Button.X:
                        logger.info("X")  # TODO
                    elif button is Button.Y:
                        logger.info("Y")
                    elif button is Button.RIGHT_BUMPER:
                        logger.info("Stopping motion")
                        camera.stop()
                    elif button is Button.LEFT_BUMPER:
                        logger.info("Stopping motion")
                        camera.stop()
            elif event.type == EventType.AXIS:
                axis: Axis = event.subject

                if axis in (Axis.D_PAD_X, Axis.D_PAD_Y):
                    if axis is Axis.D_PAD_X:
                        d_pad_x = event.value
                    elif axis is Axis.D_PAD_Y:
                        d_pad_y = event.value

                    if d_pad_y == 0 and d_pad_x == -1:
                        logger.info(f"Panning Left (speed={DEFAULT_SPEED})")
                        camera.pan_left(DEFAULT_SPEED)
                    elif d_pad_y == 0 and d_pad_x == 1:
                        logger.info(f"Panning Right (speed={DEFAULT_SPEED})")
                        camera.pan_right(DEFAULT_SPEED)
                    elif d_pad_x == 0 and d_pad_y == -1:
                        logger.info(f"Tilting Up (speed={DEFAULT_SPEED})")
                        camera.tilt_up(DEFAULT_SPEED)
                    elif d_pad_x == 0 and d_pad_y == 1:
                        logger.info(f"Tilting Down (speed={DEFAULT_SPEED})")
                        camera.tilt_down(DEFAULT_SPEED)
                    elif d_pad_y == -1 and d_pad_x == -1:
                        logger.info(f"Tilting Up and Panning Left (speed={DEFAULT_SPEED})")
                        camera.send_command_general_response(
                            camera.factory._standard(
                                up=True,
                                left=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == -1 and d_pad_x == 1:
                        logger.info(f"Tilting Up and Panning Right (speed={DEFAULT_SPEED})")
                        camera.send_command_general_response(
                            camera.factory._standard(
                                up=True,
                                right=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == 1 and d_pad_x == -1:
                        logger.info(f"Tilting Down and Panning Left (speed={DEFAULT_SPEED})")
                        camera.send_command_general_response(
                            camera.factory._standard(
                                down=True,
                                left=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == 1 and d_pad_x == 1:
                        logger.info(f"Tilting Down and Panning Right (speed={DEFAULT_SPEED})")
                        camera.send_command_general_response(
                            camera.factory._standard(
                                down=True,
                                right=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == 0 and d_pad_x == 0:
                        logger.info("Stopping motion")
                        camera.stop()
                else:
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
                            logger.info("Stopping")
                            camera.stop()
                        elif speed_x == 0 and speed_y > 0:
                            logger.info(f"Tilting Down (tilt_speed={speed_y})")
                            camera.tilt_down(speed_y)
                        elif speed_x == 0 and speed_y < 0:
                            logger.info(f"Tilting Up (tilt_speed={abs(speed_y)})")
                            camera.tilt_up(abs(speed_y))
                        elif speed_y == 0 and speed_x > 0:
                            logger.info(f"Panning Right (pan_speed={speed_x})")
                            camera.pan_right(speed_x)
                        elif speed_y == 0 and speed_x < 0:
                            logger.info(f"Panning Left (pan_speed={abs(speed_x)})")
                            camera.pan_left(abs(speed_x))
                        elif speed_x > 0 and speed_y > 0:
                            logger.info(
                                f"Tilting Down and Panning Right (tilt_speed={speed_y}, pan_speed={speed_x})"
                            )
                            camera.send_command_general_response(
                                camera.factory._standard(
                                    down=True,
                                    right=True,
                                    pan_speed=speed_x,
                                    tilt_speed=speed_y,
                                )
                            )
                        elif speed_x > 0 and speed_y < 0:
                            logger.info(
                                f"Tilting Up and Panning Right (tilt_speed={abs(speed_y)}, pan_speed={speed_x})"
                            )
                            camera.send_command_general_response(
                                camera.factory._standard(
                                    up=True,
                                    right=True,
                                    pan_speed=speed_x,
                                    tilt_speed=abs(speed_y),
                                )
                            )
                        elif speed_x < 0 and speed_y > 0:
                            logger.info(
                                f"Tilting Down and Panning Left (tilt_speed={speed_y}, pan_speed={abs(speed_x)})"
                            )
                            camera.send_command_general_response(
                                camera.factory._standard(
                                    down=True,
                                    left=True,
                                    pan_speed=abs(speed_x),
                                    tilt_speed=speed_y,
                                )
                            )
                        elif speed_x < 0 and speed_y < 0:
                            logger.info(
                                f"Tilting Up and Panning Left (tilt_speed={abs(speed_y)}, pan_speed={abs(speed_x)})"
                            )
                            camera.send_command_general_response(
                                camera.factory._standard(
                                    up=True,
                                    left=True,
                                    pan_speed=abs(speed_x),
                                    tilt_speed=abs(speed_y),
                                )
                            )
                    elif axis is Axis.LEFT_TRIGGER:
                        if event.value == 0:
                            logger.info("Stopping motion")
                            camera.stop()
                            continue

                        zoom_speed: int = trigger_value_to_zoom_speed(event.value)
                        prev_zoom_speed: int = trigger_value_to_zoom_speed(left_trigger)
                        speed_diff: int = abs(zoom_speed - prev_zoom_speed)

                        left_trigger = event.value

                        if speed_diff == 0:
                            continue

                        logger.info(f"Setting zoom speed to {zoom_speed}")
                        camera.set_zoom_speed(zoom_speed)
                        logger.info("Zooming out")
                        camera.zoom_wide()
                    elif axis is Axis.RIGHT_TRIGGER:
                        if event.value == 0:
                            logger.info("Stopping motion")
                            camera.stop()
                            continue

                        zoom_speed: int = trigger_value_to_zoom_speed(event.value)
                        prev_zoom_speed: int = trigger_value_to_zoom_speed(right_trigger)
                        speed_diff: int = abs(zoom_speed - prev_zoom_speed)

                        right_trigger = event.value

                        if speed_diff == 0:
                            continue

                        logger.info(f"Setting zoom speed to {zoom_speed}")
                        camera.set_zoom_speed(zoom_speed)
                        logger.info("Zooming in")
                        camera.zoom_tele()
    except ResponseError as error:
        logger.error("Camera did not send a response, try again.")
        continue
    except OSError as error:
        # XBox controller has disconnected, retrying.
        continue
