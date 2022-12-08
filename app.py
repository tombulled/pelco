from functools import reduce

import serial
import serial.tools.list_ports

import pelco

import time

assert serial.tools.list_ports.comports()[0].product == "FT232R USB UART"

ADDRESS = b"\x02"

# Serial Data Format
# Baudrate: 2400, 4800, 9600, 19200, 38400, 115200
# StartBit: 1
# DataLength: 8
# StopBit: 1
# Parity: None

s = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=2400
)

def calc_crc(command: bytes) -> str:
    return hex(reduce(lambda x,y:x+y, map(lambda x:x, command)) % 256)[2:].upper().zfill(2)

def send_command(command: str) -> None:
    mid_section = ADDRESS + bytearray.fromhex(command)
    crc = calc_crc(mid_section)
    full_command = b"\xFF" + mid_section + int(crc, 16).to_bytes(1, 'big')
    s.write(full_command)
    # return s.read(4)

def up() -> None:
    return send_command("00 08 00 27")

def down() -> None:
    return send_command("00 10 00 27")

def left() -> None:
    return send_command("00 04 3F 00")

def right() -> None:
    return send_command("00 02 3F 00")

def stop() -> None:
    return send_command("00 00 00 00")

def up_right() -> None:
    return send_command("00 0A 27 27")

def down_right() -> None:
    return send_command("00 12 27 27")

def zoom_in() -> None:
    return send_command("00 20 00 00")

def zoom_out() -> None:
    return send_command("00 40 00 00")

def iris_close() -> None:
    return send_command("04 00 00 00")

def iris_open() -> None:
    return send_command("02 00 00 00")

def focus_near() -> None:
    return send_command("01 00 00 00")

def focus_far() -> None:
    return send_command("00 80 00 00")

p = pelco.Pelco(address=0x02)