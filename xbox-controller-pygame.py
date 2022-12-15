from enum import Enum, IntEnum, auto

import pygame

from pelco.d.master import PelcoD


class Event(Enum):
    BUTTON_DOWN = auto()
    BUTTON_UP = auto()
    HAT_MOTION = auto()
    AXIS_MOTION = auto()
    DEVICE_ADDED = auto()
    DEVICE_REMOVED = auto()


class Button(IntEnum):
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    LEFT_BUMPER: int = 4
    RIGHT_BUMPER: int = 5
    VIEW: int = 6
    MENU: int = 7
    HOME: int = 8
    LEFT_STICK: int = 9
    RIGHT_STICK: int = 10


class Axis(IntEnum):
    LEFT_STICK_X: int = 0
    LEFT_STICK_Y: int = 1
    LEFT_TRIGGER: int = 2
    RIGHT_STICK_X: int = 3
    RIGHT_STICK_Y: int = 4
    RIGHT_TRIGGER: int = 5


class Hat(IntEnum):
    DIRECTIONAL_PAD: int = 0


# Initialise pygame
pygame.init()

joysticks = [
    pygame.joystick.Joystick(index) for index in range(pygame.joystick.get_count())
]

# Ensure XBox Controller connected
assert joysticks and joysticks[0].get_name() == "Xbox One S Controller"


while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            button: Button = Button(event.button)

            print(f"Button Down: {button.name}")
        elif event.type == pygame.JOYBUTTONUP:
            button: Button = Button(event.button)

            print(f"Button Up: {button.name}")
        elif event.type == pygame.JOYHATMOTION:
            hat: Hat = Hat(event.hat)

            if event.value == (-1, 0):
                hm = "Left"
            elif event.value == (1, 0):
                hm = "Right"
            elif event.value == (0, 1):
                hm = "Up"
            elif event.value == (0, -1):
                hm = "Down"
            elif event.value == (0, 0):
                hm = "Nothing"
            elif event.value == (-1, 1):
                hm = "Up-Left"
            elif event.value == (-1, -1):
                hm = "Down-Left"
            elif event.value == (1, -1):
                hm = "Down-Right"
            elif event.value == (1, 1):
                hm = "Up-Right"
            else:
                hm = "Unknown"

            print(f"Joystick Hat Motion: {hat.name} -> {event.value}")
        elif event.type == pygame.JOYAXISMOTION:
            axis: Axis = Axis(event.axis)

            print(f"Joystick Axis Motion: {axis.name} -> {event.value}")
        elif event.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(event.device_index)
            joysticks[joystick.get_instance_id()] = joystick

            print(f"Joystick Added: {joystick.get_name()}")
        elif event.type == pygame.JOYDEVICEREMOVED:
            joystick = joysticks[event.instance_id]
            del joysticks[event.instance_id]

            print(f"Joystick Removed: {joystick.get_name()}")
        else:
            continue
