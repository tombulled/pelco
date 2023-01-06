from typing import MutableSequence, Sequence

import inputs
from inputs import GamePad

from .controller import XBoxOneController


def find_controllers() -> Sequence[XBoxOneController]:
    controllers: MutableSequence[XBoxOneController] = []

    gamepad: GamePad
    for gamepad in inputs.devices.gamepads:
        if gamepad.name == "Microsoft X-Box One S pad":
            controllers.append(XBoxOneController(gamepad.get_char_device_path()))

    return controllers
