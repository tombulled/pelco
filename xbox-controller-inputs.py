from typing import Callable, Optional, Sequence
import time

import serial.tools.list_ports
from loguru import logger
from pelco.d.constants import PRESET_FLIP
from pelco.d.errors import ResponseError
from pelco.d.master import PelcoD
from xboxonecontroller.controller import XBoxOneController
from xboxonecontroller.enums import Axis, Button, EventType

TRIGGER_MAX: int = 2**10
STICK_MAX: int = 2**15

# Pan and tilt speed
SPEED_MIN: int = 0x1F # can't be 0 as breaks logic
SPEED_MAX: int = 0x3F
SPEED_STEP: int = 0x01

ZOOM_SPEED_MIN: int = 0x00
ZOOM_SPEED_MAX: int = 0x03
ZOOM_SPEED_STEP: int = 0x01

STICK_THRESHOLD: float = 0.17  # Ignore the first n%. Has been observed as high as ~20%

# To ensure that no "confusion" occurs in the Pelco receiving equipment, a delay of at
# least 300 milliseconds must be inserted between sending commands
# SEND_COMMAND_DELAY: float = 0.3 # Delay in seconds
SEND_COMMAND_DELAY: int = 300 # Delay in ms

def delay() -> None:
    time.sleep(0.3)


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
factory = camera.factory
# camera = FakeCamera()

XBOX_CONTROLLER_DEVICE_PATH: str = "/dev/input/by-id/usb-Microsoft_Controller_3032363030303037393636363230-event-joystick"

xbox_controller = XBoxOneController(device_path=XBOX_CONTROLLER_DEVICE_PATH)

DEFAULT_SPEED: int = 0x1F


def stick_value_to_speed(value: int, /) -> Optional[int]:
    speeds: Sequence[int] = tuple(
        range(SPEED_MIN, SPEED_MAX + 1, SPEED_STEP)
    )
    max_index: int = len(speeds) - 1
    sign: int = -1 if value < 0 else 1
    normalised_value: float = abs(value) / STICK_MAX

    if normalised_value <= STICK_THRESHOLD:
        return None

    speed_index: int = round(normalised_value * max_index)

    return sign * speeds[speed_index]


def trigger_value_to_zoom_speed(value: int, /) -> int:
    zoom_speeds: Sequence[int] = tuple(
        range(ZOOM_SPEED_MIN, ZOOM_SPEED_MAX + 1, ZOOM_SPEED_STEP)
    )
    max_index: int = len(zoom_speeds) - 1
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
in_motion: bool = False
last_motion: float = 0

while True:
    try:
        for event in xbox_controller.read():
            event_time: float = time.time()

            if event.type == EventType.BUTTON:
                button: Button = event.subject
                down: bool = bool(event.value)

                if down:
                    if button is Button.RIGHT_BUMPER:
                        logger.info("Starting Focus Near")
                        camera.send(factory.focus_near())
                    elif button is Button.LEFT_BUMPER:
                        logger.info("Starting Focus Far")
                        camera.send(factory.focus_far())
                else:
                    if button is Button.MENU:
                        logger.info("Opening menu")
                        camera.send(factory.set_preset(95))
                    elif button is Button.VIEW:
                        logger.info("VIEW")
                    elif button is Button.A:
                        logger.info("A")
                    elif button is Button.B:  # Note: pointless as could flick a button?
                        logger.info("Stopping motion")
                        camera.send(factory.stop())
                        camera.send(factory.stop())
                    elif button is Button.X:
                        logger.info("X")
                    elif button is Button.Y:
                        logger.info("Flipping 180 degrees")
                        camera.send(factory.move_preset(PRESET_FLIP))
                    elif button is Button.RIGHT_BUMPER:
                        logger.info("Stopping motion")
                        camera.send(factory.stop())
                    elif button is Button.LEFT_BUMPER:
                        logger.info("Stopping motion")
                        camera.send(factory.stop())
            elif event.type == EventType.AXIS:
                axis: Axis = event.subject

                # print(f"Axis Movement: {axis.name} -> {event.value}")

                if axis in (Axis.D_PAD_X, Axis.D_PAD_Y):
                    if axis is Axis.D_PAD_X:
                        d_pad_x = event.value
                    elif axis is Axis.D_PAD_Y:
                        d_pad_y = event.value

                    if d_pad_y == 0 and d_pad_x == -1:
                        logger.info(f"Panning Left (speed={DEFAULT_SPEED})")
                        camera.send(factory.pan_left(DEFAULT_SPEED))
                    elif d_pad_y == 0 and d_pad_x == 1:
                        logger.info(f"Panning Right (speed={DEFAULT_SPEED})")
                        camera.send(factory.pan_right(DEFAULT_SPEED))
                    elif d_pad_x == 0 and d_pad_y == -1:
                        logger.info(f"Tilting Up (speed={DEFAULT_SPEED})")
                        camera.send(factory.tilt_up(DEFAULT_SPEED))
                    elif d_pad_x == 0 and d_pad_y == 1:
                        logger.info(f"Tilting Down (speed={DEFAULT_SPEED})")
                        camera.send(factory.tilt_down(DEFAULT_SPEED))
                    elif d_pad_y == -1 and d_pad_x == -1:
                        logger.info(
                            f"Tilting Up and Panning Left (speed={DEFAULT_SPEED})"
                        )
                        camera.send(
                            camera.factory._standard(
                                up=True,
                                left=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == -1 and d_pad_x == 1:
                        logger.info(
                            f"Tilting Up and Panning Right (speed={DEFAULT_SPEED})"
                        )
                        camera.send(
                            camera.factory._standard(
                                up=True,
                                right=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == 1 and d_pad_x == -1:
                        logger.info(
                            f"Tilting Down and Panning Left (speed={DEFAULT_SPEED})"
                        )
                        camera.send(
                            camera.factory._standard(
                                down=True,
                                left=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == 1 and d_pad_x == 1:
                        logger.info(
                            f"Tilting Down and Panning Right (speed={DEFAULT_SPEED})"
                        )
                        camera.send(
                            camera.factory._standard(
                                down=True,
                                right=True,
                                pan_speed=DEFAULT_SPEED,
                                tilt_speed=DEFAULT_SPEED,
                            )
                        )
                    elif d_pad_y == 0 and d_pad_x == 0:
                        logger.info("Stopping motion")
                        camera.send(factory.stop())
                else:
                    if axis in (Axis.LEFT_STICK_X, Axis.LEFT_STICK_Y):
                        pre_left_stick_x: int = left_stick_x
                        pre_left_stick_y: int = left_stick_y
                        speed_dx: int = 0
                        speed_dy: int = 0

                        if axis is Axis.LEFT_STICK_X:
                            left_stick_x = event.value

                            pre_speed: int = stick_value_to_speed(pre_left_stick_x) or 0
                            speed: int = stick_value_to_speed(left_stick_x) or 0

                            speed_dx = abs(
                                abs(pre_speed)
                                - abs(speed)
                            )
                        elif axis is Axis.LEFT_STICK_Y:
                            left_stick_y = event.value

                            pre_speed: int = stick_value_to_speed(pre_left_stick_y) or 0
                            speed: int = stick_value_to_speed(left_stick_y) or 0

                            speed_dy = abs(
                                abs(pre_speed)
                                - abs(speed)
                            )

                        speed_x: Optional[int] = stick_value_to_speed(left_stick_x)
                        speed_y: Optional[int] = stick_value_to_speed(left_stick_y)

                        if speed_x is None and speed_y is None:
                            if in_motion:
                                logger.info("Stopping motion")
                                delay()
                                camera.send(factory.stop())
                                camera.send(factory.stop())
                                in_motion = False
                                last_motion = time.time()
                            continue

                        if speed_dx == 0 and speed_dy == 0:
                            # No significant difference, ignoring.
                            continue

                        print("Time since last movement (ms):", round((event_time - last_motion) * 1000))

                        # Motion event received too soon, ignoring.
                        if round((event_time - last_motion) * 1000) < SEND_COMMAND_DELAY:
                            continue


                        if speed_x is None and speed_y > 0:
                            logger.info(f"Tilting Down (tilt_speed={speed_y})")
                            camera.send(factory.tilt_down(speed_y))
                            in_motion = True
                            last_motion = time.time()
                        elif speed_x is None and speed_y < 0:
                            logger.info(f"Tilting Up (tilt_speed={abs(speed_y)})")
                            camera.send(factory.tilt_up(abs(speed_y)))
                            in_motion = True
                            last_motion = time.time()
                        elif speed_y is None and speed_x > 0:
                            logger.info(f"Panning Right (pan_speed={speed_x})")
                            camera.send(factory.pan_right(speed_x))
                            in_motion = True
                            last_motion = time.time()
                        elif speed_y is None and speed_x < 0:
                            logger.info(f"Panning Left (pan_speed={abs(speed_x)})")
                            camera.send(factory.pan_left(abs(speed_x)))
                            in_motion = True
                            last_motion = time.time()
                        elif speed_x > 0 and speed_y > 0:
                            logger.info(
                                f"Tilting Down and Panning Right (tilt_speed={speed_y}, pan_speed={speed_x})"
                            )
                            camera.send(
                                camera.factory._standard(
                                    down=True,
                                    right=True,
                                    pan_speed=speed_x,
                                    tilt_speed=speed_y,
                                )
                            )
                            in_motion = True
                            last_motion = time.time()
                        elif speed_x > 0 and speed_y < 0:
                            logger.info(
                                f"Tilting Up and Panning Right (tilt_speed={abs(speed_y)}, pan_speed={speed_x})"
                            )
                            camera.send(
                                camera.factory._standard(
                                    up=True,
                                    right=True,
                                    pan_speed=speed_x,
                                    tilt_speed=abs(speed_y),
                                )
                            )
                            in_motion = True
                            last_motion = time.time()
                        elif speed_x < 0 and speed_y > 0:
                            logger.info(
                                f"Tilting Down and Panning Left (tilt_speed={speed_y}, pan_speed={abs(speed_x)})"
                            )
                            camera.send(
                                camera.factory._standard(
                                    down=True,
                                    left=True,
                                    pan_speed=abs(speed_x),
                                    tilt_speed=speed_y,
                                )
                            )
                            in_motion = True
                            last_motion = time.time()
                        elif speed_x < 0 and speed_y < 0:
                            logger.info(
                                f"Tilting Up and Panning Left (tilt_speed={abs(speed_y)}, pan_speed={abs(speed_x)})"
                            )
                            camera.send(
                                camera.factory._standard(
                                    up=True,
                                    left=True,
                                    pan_speed=abs(speed_x),
                                    tilt_speed=abs(speed_y),
                                )
                            )
                            in_motion = True
                            last_motion = time.time()
                    elif axis is Axis.LEFT_TRIGGER:
                        if event.value == 0:
                            logger.info("Stopping motion")
                            camera.send(factory.stop())
                            continue

                        zoom_speed: int = trigger_value_to_zoom_speed(event.value)
                        prev_zoom_speed: int = trigger_value_to_zoom_speed(left_trigger)
                        speed_diff: int = abs(zoom_speed - prev_zoom_speed)

                        left_trigger = event.value

                        if speed_diff == 0:
                            continue

                        logger.info(f"Setting zoom speed to {zoom_speed}")
                        camera.send(factory.set_zoom_speed(zoom_speed))
                        logger.info("Zooming out")
                        camera.send(factory.zoom_wide())
                    elif axis is Axis.RIGHT_TRIGGER:
                        if event.value == 0:
                            logger.info("Stopping motion")
                            camera.send(factory.stop())
                            continue

                        zoom_speed: int = trigger_value_to_zoom_speed(event.value)
                        prev_zoom_speed: int = trigger_value_to_zoom_speed(
                            right_trigger
                        )
                        speed_diff: int = abs(zoom_speed - prev_zoom_speed)

                        right_trigger = event.value

                        if speed_diff == 0:
                            continue

                        logger.info(f"Setting zoom speed to {zoom_speed}")
                        camera.send(factory.set_zoom_speed(zoom_speed))
                        logger.info("Zooming in")
                        camera.send(factory.zoom_tele())
    except ResponseError as error:
        logger.error(error)
        continue
    except OSError as error:
        logger.error(error)

        # XBox controller has disconnected, attempt to reconnect.
        try:
            xbox_controller = XBoxOneController(device_path=XBOX_CONTROLLER_DEVICE_PATH)
        except Exception as error:
            # XBox controller not available, give up for now.
            logger.error(error)
            continue
