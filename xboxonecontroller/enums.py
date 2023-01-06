from enum import Enum, auto


class NoValue(Enum):
    def __repr__(self) -> str:
        return f"<{type(self).__name__}.{self.name}>"


class EventType(NoValue):
    BUTTON = auto()
    AXIS = auto()


class Button(NoValue):
    A = auto()
    B = auto()
    X = auto()
    Y = auto()
    LEFT_BUMPER = auto()
    RIGHT_BUMPER = auto()
    VIEW = auto()
    MENU = auto()
    HOME = auto()
    LEFT_STICK = auto()
    RIGHT_STICK = auto()


class Axis(NoValue):
    D_PAD_X = auto()
    D_PAD_Y = auto()
    LEFT_STICK_X = auto()
    LEFT_STICK_Y = auto()
    LEFT_TRIGGER = auto()
    RIGHT_STICK_X = auto()
    RIGHT_STICK_Y = auto()
    RIGHT_TRIGGER = auto()
