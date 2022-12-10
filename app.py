import serial.tools.list_ports

import pelco

# Ensure the USB TO RS485 converter is plugged in
comports = serial.tools.list_ports.comports()
assert comports and comports[0].product == "FT232R USB UART"

p = pelco.Pelco(address=0x02)

ok = lambda: p.focus_near()
up = lambda: p.tilt_up()
down = lambda: p.tilt_down()
left = lambda: p.pan_left()
right = lambda: p.pan_right()