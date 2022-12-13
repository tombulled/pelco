import serial.tools.list_ports

import pelco
import pelco.d
import pelco.p
from pelco.d.master import PelcoD


def get_device() -> str:
    comports = serial.tools.list_ports.comports()

    for comport in comports:
        if comport.product == "FT232R USB UART":
            return comport.device

    raise Exception("Failed to find serial device")


device: str = get_device()

p = PelcoD(
    address=0x02,
    port=device,
)

SPEED: int = 0x00

commands = {
    "fn": lambda: p.focus_near(),  # focus near
    "ff": lambda: p.focus_far(),  # focus far
    "zt": lambda: p.zoom_tele(),  # zoom tele
    "zw": lambda: p.zoom_wide(),  # zoom wide
    "u": lambda: p.tilt_up(SPEED),  # tilt up
    "d": lambda: p.tilt_down(SPEED),  # tilt down
    "l": lambda: p.pan_left(SPEED),  # pan left
    "r": lambda: p.pan_right(SPEED),  # pan right
    "": lambda: p.stop(),  # stop
    "ws": lambda: p.set_auxiliary(1),  # start wiper
    "we": lambda: p.clear_auxiliary(1),  # stop wiper
    "180": lambda: p.flip_180_about(),  # flip 180 degrees
    "sp1": lambda: p.set_preset(1),  # set preset 1
    "sp2": lambda: p.set_preset(2),  # set preset 1
    "sp3": lambda: p.set_preset(3),  # set preset 1
    "gp1": lambda: p.go_to_preset(1),  # go to preset 1
    "gp2": lambda: p.go_to_preset(2),  # go to preset 1
    "gp3": lambda: p.go_to_preset(3),  # go to preset 1
}

while True:
    command: str = input("> ")

    if command not in commands:
        print(f"Unrecognised command: {command!r}")
        continue

    commands[command]()
