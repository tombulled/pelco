from typing import MutableSequence, Optional, Sequence

import inputs
from inputs import GamePad, InputEvent

from . import utils
from .errors import InvalidDevicePath
from .models import Event


def get_gamepad(device_path: str) -> GamePad:
    gamepad: GamePad
    for gamepad in inputs.devices.gamepads:
        if (
            gamepad.get_char_device_path() == device_path
            or gamepad._device_path == device_path
        ):
            return gamepad

    raise InvalidDevicePath(f"Invalid device path: {device_path!r}")


class XBoxOneController:
    _gamepad: GamePad

    def __init__(self, device_path: str) -> None:
        self._gamepad = get_gamepad(device_path)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(device_path={self._gamepad.get_char_device_path()!r})"

    def read(self) -> Sequence[Event]:
        events: MutableSequence[Event] = []

        input_event: InputEvent
        for input_event in self._gamepad.read():
            event: Optional[Event] = utils.convert_event(input_event)

            if event is not None:
                events.append(event)

        return events
