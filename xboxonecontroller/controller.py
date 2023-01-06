from typing import MutableSequence, Optional, Sequence

from inputs import DeviceManager, GamePad, InputEvent

from . import utils
from .models import Event


class XBoxOneController:
    _gamepad: GamePad

    def __init__(self, device_path: str) -> None:
        device_manager: DeviceManager = DeviceManager()
        self._gamepad = GamePad(manager=device_manager, device_path=device_path)

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
