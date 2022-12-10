import serial.tools.list_ports

import pelco

# Ensure the USB TO RS485 converter is plugged in
comports = serial.tools.list_ports.comports()
assert comports and comports[0].product == "FT232R USB UART"

p = pelco.Pelco(address=0x02)

f = lambda: p.focus_near()
u = lambda: p.tilt_up()
d = lambda: p.tilt_down()
l = lambda: p.pan_left()
r = lambda: p.pan_right()
s = lambda: p.stop()
g = lambda i: p.go_to_preset(i)