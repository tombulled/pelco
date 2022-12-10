import serial.tools.list_ports

import pelco

# Ensure the USB TO RS485 converter is plugged in
comports = serial.tools.list_ports.comports()
assert comports and comports[0].product == "FT232R USB UART"

p = pelco.Pelco(address=0x02)

commands = {
    "fn": lambda: p.focus_near(), # focus near
    "ff": lambda: p.focus_far(), # focus far
    "zt": lambda: p.zoom_tele(), # zoom tele
    "zw": lambda: p.zoom_wide(), # zoom wide
    "u": lambda: p.tilt_up(), # tilt up
    "d": lambda: p.tilt_down(), # tilt down
    "l": lambda: p.pan_left(), # pan left
    "r": lambda: p.pan_right(), # pan right
    "": lambda: p.stop(), # stop
    "ws": lambda: p.set_auxiliary(1), # start wiper
    "we": lambda: p.clear_auxiliary(1), # stop wiper
    "180": lambda: p.flip_180_about(), # flip 180 degrees
    "sp1": lambda: p.set_preset(1), # set preset 1
    "sp2": lambda: p.set_preset(2), # set preset 1
    "sp3": lambda: p.set_preset(3), # set preset 1
    "gp1": lambda: p.go_to_preset(1), # go to preset 1
    "gp2": lambda: p.go_to_preset(2), # go to preset 1
    "gp3": lambda: p.go_to_preset(3), # go to preset 1
}

while True:
    command: str = input("> ")

    if command not in commands:
        print(f"Unrecognised command: {command!r}")
        continue

    commands[command]()