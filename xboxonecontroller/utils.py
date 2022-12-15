from typing import Optional

from inputs import InputEvent

from . import mappings
from .enums import Axis, Button, EventType
from .models import Event


def get_button(event_code: str, /) -> Button:
    return mappings.button_mapping[event_code]


def get_axis(event_code: str, /) -> Axis:
    return mappings.axis_mapping[event_code]


def convert_event(event: InputEvent, /) -> Optional[Event]:
    if event.ev_type == "Key":
        return Event(
            type=EventType.BUTTON,
            subject=get_button(event.code),
            value=event.state,
        )
    elif event.ev_type == "Absolute":
        return Event(
            type=EventType.AXIS,
            subject=get_axis(event.code),
            value=event.state,
        )
    else:
        return None
