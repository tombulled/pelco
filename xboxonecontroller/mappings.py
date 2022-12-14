from typing import Mapping

from .enums import Axis, Button

button_mapping: Mapping[str, Button] = {
    "BTN_SOUTH": Button.A,
    "BTN_EAST": Button.B,
    "BTN_NORTH": Button.X,
    "BTN_WEST": Button.Y,
    "BTN_TL": Button.LEFT_BUMPER,
    "BTN_TR": Button.RIGHT_BUMPER,
    "BTN_SELECT": Button.VIEW,
    "BTN_START": Button.MENU,
    "BTN_MODE": Button.HOME,
    "BTN_THUMBL": Button.LEFT_STICK,
    "BTN_THUMBR": Button.RIGHT_STICK,
}

axis_mapping: Mapping[str, Axis] = {
    "ABS_HAT0X": Axis.D_PAD_X,
    "ABS_HAT0Y": Axis.D_PAD_Y,
    "ABS_X": Axis.LEFT_STICK_X,
    "ABS_Y": Axis.LEFT_STICK_Y,
    "ABS_Z": Axis.LEFT_TRIGGER,
    "ABS_RX": Axis.RIGHT_STICK_X,
    "ABS_RY": Axis.RIGHT_STICK_Y,
    "ABS_RZ": Axis.RIGHT_TRIGGER,
}