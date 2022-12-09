from dataclasses import dataclass

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


@dataclass(frozen=True, eq=True)
class ExtendedResponse:
    sync: int = SYNC  # SYNC
    address: int = 0x00  # ADDR
    response_1: int = 0x00  # RESP1
    response_2: int = 0x00  # RESP2
    data_1: int = 0x00  # DATA1
    data_2: int = 0x00  # DATA2
    checksum: int = 0x00  # CKSM


@dataclass(frozen=True, eq=True)
class QueryResponse:
    ...
