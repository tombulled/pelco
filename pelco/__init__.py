from dataclasses import dataclass
from enum import Enum, IntEnum

import serial

from .constants import SYNC


@dataclass(frozen=True, eq=True)
class SendCommandModel:
    # sync: int = SYNC  # SYNC
    address: int = 0x00  # ADDR
    command_1: int = 0x00  # CMND1
    command_2: int = 0x00  # CMND2
    data_1: int = 0x00  # DATA1
    data_2: int = 0x00  # DATA2
    # checksum: int = 0x00  # CKSM

    def calculate_crc(self) -> int:
        return sum(
            (
                self.address,
                self.command_1,
                self.command_2,
                self.data_1,
                self.data_2,
            )
        ) % (0xFF + 1)

    def serialise(self) -> bytearray:
        return bytearray(
            (
                SYNC,
                self.address,
                self.command_1,
                self.command_2,
                self.data_1,
                self.data_2,
                self.calculate_crc(),
            )
        )

    @classmethod
    def deserialise(cls, command: bytes, /) -> "SendCommandModel":
        assert len(command) == 7
        assert command[0] == SYNC

        model: SendCommandModel = cls(
            address=command[1],
            command_1=command[2],
            command_2=command[3],
            data_1=command[4],
            data_2=command[5],
        )

        assert model.calculate_crc() == command[6]

        return model


@dataclass(frozen=True, eq=True)
class GeneralResponse:
    sync: int = SYNC  # SYNC
    address: int = 0x00  # ADDR
    alarms: int = 0x00  # ALARMS
    checksum: int = 0x00  # CKSM

    def serialise(self) -> bytearray:
        return bytearray(
            (
                self.sync,
                self.address,
                self.alarms,
                self.checksum,
            )
        )

    @classmethod
    def deserialise(cls, command: bytes, /) -> "GeneralResponse":
        assert len(command) == 4

        model: GeneralResponse = cls(
            sync=command[0],
            address=command[1],
            alarms=command[2],
            checksum=command[3],
        )

        return model


# aka "CMND1"
class ExtensionCommand(IntEnum):
    SENSE = 0b10000000
    RESERVED_6 = 0b01000000
    RESERVED_5 = 0b00100000
    SCAN = 0b00010000
    CAMERA = 0b00001000
    IRIS_CLOSE = 0b00000100
    IRIS_OPEN = 0b00000010
    FOCUS_NEAR = 0b00000001


# aka "CMND2"
class StandardCommand(IntEnum):
    ...


class SendCommand(Enum):
    command_1: int
    command_2: int

    # Standard Commands
    STOP = (0x00, 0x00)
    RIGHT = (0x00, 0x02)
    LEFT = (0x00, 0x04)
    UP = (0x00, 0x08)
    DOWN = (0x00, 0x10)
    ZOOM_TELE = (0x00, 0x20)
    ZOOM_WIDE = (0x00, 0x40)
    FOCUS_FAR = (0x00, 0x80)
    FOCUS_NEAR = (0x01, 0x00)
    IRIS_OPEN = (0x02, 0x00)
    IRIS_CLOSE = (0x04, 0x00)

    # Extended Commands
    SET_ZOOM_SPEED = (0x00, 0x25)
    # ...

    def __init__(self, command_1: int, command_2: int, /) -> None:
        self.command_1 = command_1
        self.command_2 = command_2


class Speed(IntEnum):
    VERY_SLOW = 0x00
    SLOW = 0x0F
    MEDIUM = 0x1F
    FAST = 0x2F
    VERY_FAST = 0x3F


SENSE = 0b10000000
RESERVED_6 = 0b01000000
RESERVED_5 = 0b00100000
SCAN = 0b00010000
CAMERA = 0b00001000
IRIS_CLOSE = 0b00000100
IRIS_OPEN = 0b00000010
FOCUS_NEAR = 0b00000001

FOCUS_FAR = 0b10000000
ZOOM_WIDE = 0b01000000
ZOOM_TELE = 0b00100000
DOWN = 0b00010000
UP = 0b00001000
LEFT = 0b00000100
RIGHT = 0b00000010
RESERVED_0 = 0b00000001


@dataclass
class SendCommandFactory:
    address: int = 0x01

    def camera_on(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=SENSE | CAMERA,
        )

    def camera_off(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=CAMERA,
        )

    def scan_auto(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=SENSE | SCAN,
        )

    def scan_manual(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=SCAN,
        )

    def iris_close(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=IRIS_CLOSE,
        )

    def iris_open(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=IRIS_OPEN,
        )

    def stop(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
        )

    def pan_right(self, speed: int) -> SendCommandModel:
        assert 0 <= speed <= 0x3F

        return SendCommandModel(
            address=self.address,
            command_2=RIGHT,
            data_1=speed,
        )

    def pan_left(self, speed: int) -> SendCommandModel:
        assert 0 <= speed <= 0x3F

        return SendCommandModel(
            address=self.address,
            command_2=LEFT,
            data_1=speed,
        )

    def tilt_up(self, speed: int) -> SendCommandModel:
        assert 0 <= speed <= 0x3F

        return SendCommandModel(
            address=self.address,
            command_2=UP,
            data_2=speed,
        )

    def tilt_down(self, speed: int) -> SendCommandModel:
        assert 0 <= speed <= 0x3F

        return SendCommandModel(
            address=self.address,
            command_2=DOWN,
            data_2=speed,
        )

    def zoom_tele(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=ZOOM_TELE,
        )

    def zoom_wide(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=ZOOM_WIDE,
        )

    def focus_far(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_2=FOCUS_FAR,
        )

    def focus_near(self) -> SendCommandModel:
        return SendCommandModel(
            address=self.address,
            command_1=FOCUS_NEAR,
        )


class Pelco:
    address: int

    def __init__(self, address: int = 0x01) -> None:
        self.address = address

        self.command_factory = SendCommandFactory(address=address)
        self.s = serial.Serial(port="/dev/ttyUSB0", baudrate=2400)

    def send_standard_command(self, command: SendCommandModel, /) -> GeneralResponse:
        self.s.write(command.serialise())

        return GeneralResponse.deserialise(self.s.read(4))

    def camera_on(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.camera_on())

    def camera_off(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.camera_off())

    def camera(self, on: bool) -> GeneralResponse:
        if on:
            return self.camera_on()
        else:
            return self.camera_off()

    def scan_auto(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.scan_auto())

    def scan_manual(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.scan_manual())

    def scan(self, auto: bool) -> GeneralResponse:
        if auto:
            return self.scan_auto()
        else:
            return self.scan_manual()

    def iris_close(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.iris_close())

    def iris_open(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.iris_open())

    def stop(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.stop())

    def pan_right(self, speed: int = Speed.MEDIUM) -> GeneralResponse:
        assert 0 <= speed <= 0x3F

        return self.send_standard_command(self.command_factory.pan_right(speed))

    def pan_left(self, speed: int = Speed.MEDIUM) -> GeneralResponse:
        assert 0 <= speed <= 0x3F

        return self.send_standard_command(self.command_factory.pan_left(speed))

    def pan(self, speed: int) -> GeneralResponse:
        if speed > 0:
            return self.pan_right(speed=speed)
        elif speed < 0:
            return self.pan_left(speed=-speed)
        else:
            return self.stop()

    def tilt_up(self, speed: int = Speed.MEDIUM) -> GeneralResponse:
        assert 0 <= speed <= 0x3F

        return self.send_standard_command(self.command_factory.tilt_up(speed))

    def tilt_down(self, speed: int = Speed.MEDIUM) -> GeneralResponse:
        assert 0 <= speed <= 0x3F

        return self.send_standard_command(self.command_factory.tilt_down(speed))

    def tilt(self, speed: int) -> GeneralResponse:
        if speed > 0:
            return self.tilt_up(speed=speed)
        elif speed < 0:
            return self.tilt_down(speed=-speed)
        else:
            return self.stop()

    def zoom_tele(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.zoom_tele())

    def zoom_wide(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.zoom_wide())

    def zoom(self, tele: bool = True) -> GeneralResponse:
        if tele:
            return self.zoom_tele()
        else:
            return self.zoom_wide()

    def focus_far(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.focus_far())

    def focus_near(self) -> GeneralResponse:
        return self.send_standard_command(self.command_factory.focus_near())

    def focus(self, near: bool = True) -> GeneralResponse:
        if near:
            return self.focus_near()
        else:
            return self.focus_far()
