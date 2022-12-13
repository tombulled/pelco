from dataclasses import dataclass

from .constants import SYNC
from .errors import ResponseError
from .utils import calculate_checksum


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
        return calculate_checksum((
            self.address,
                self.command_1,
                self.command_2,
                self.data_1,
                self.data_2,
        ))

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


# aka. "General Reply"
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
    def deserialise(cls, response: bytes, /) -> "GeneralResponse":
        expected_response_length: int = 4
        response_length: int = len(response)

        if len(response) != expected_response_length:
            raise ResponseError(
                f"Expected response of length {expected_response_length}, got response of length {response_length}"
            )

        sync: int
        address: int
        alarms: int
        checksum: int
        sync, address, alarms, checksum = response

        if sync != SYNC:
            raise ResponseError(f"Invalid sync byte, expected {SYNC!r}, got {sync!r}")

        # TODO: Check checksum here

        model: GeneralResponse = cls(
            sync=sync,
            address=address,
            alarms=alarms,
            checksum=checksum,
        )

        return model


# aka. "Extended Reply"
@dataclass(frozen=True, eq=True)
class ExtendedResponse:
    sync: int = SYNC  # SYNC
    address: int = 0x00  # ADDR
    response_1: int = 0x00  # RESP1
    response_2: int = 0x00  # RESP2
    data_1: int = 0x00  # DATA1
    data_2: int = 0x00  # DATA2
    checksum: int = 0x00  # CKSM

    def serialise(self) -> bytearray:
        return bytearray(
            (
                self.sync,
                self.address,
                self.response_1,
                self.response_2,
                self.data_1,
                self.data_2,
                self.checksum,
            )
        )

    @classmethod
    def deserialise(cls, response: bytes, /) -> "ExtendedResponse":
        expected_response_length: int = 7
        response_length: int = len(response)

        if len(response) != expected_response_length:
            raise ResponseError(
                f"Expected response of length {expected_response_length}, got response of length {response_length}"
            )

        sync: int
        address: int
        response_1: int
        response_2: int
        data_1: int
        data_2: int
        checksum: int
        sync, address, response_1, response_2, data_1, data_2, checksum = response

        if sync != SYNC:
            raise ResponseError(f"Invalid sync byte, expected {SYNC!r}, got {sync!r}")

        # TODO: Check checksum here

        model: ExtendedResponse = cls(
            sync=sync,
            address=address,
            response_1=response_1,
            response_2=response_2,
            data_1=data_1,
            data_2=data_2,
            checksum=checksum,
        )

        return model


@dataclass(frozen=True, eq=True)
class QueryResponse:
    sync: int = SYNC  # SYNC
    address: int = 0x00  # ADDR
    data_1: int = 0x00  # DATA1
    # ...
    data_15: int = 0x00  # DATA15
    checksum: int = 0x00  # CKSM
