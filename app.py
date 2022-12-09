import serial.tools.list_ports

import pelco

# Ensure the USB TO RS485 converter is plugged in
comports = serial.tools.list_ports.comports()
assert comports and comports[0].product == "FT232R USB UART"

p = pelco.Pelco(address=0x02)
