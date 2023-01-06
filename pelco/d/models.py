from dataclasses import dataclass, field
from typing import Iterable, Sequence, Tuple, Union

from .constants import (
    D_COMMAND_ADDR,
    D_COMMAND_CKSM,
    D_COMMAND_CMD1,
    D_COMMAND_CMD2,
    D_COMMAND_DATA1,
    D_COMMAND_DATA2,
    D_COMMAND_SYNC,
    D_SEND_COMMAND_LENGTH,
    DEFAULT_ADDRESS,
    SYNC,
    UNSET,
)
from .errors import ResponseError
from .utils import calculate_checksum
from .validators import validate_address, validate_all_uint8


@dataclass(unsafe_hash=True, init=False)
class PelcoDCommand:
    sync: int
    address: int
    command_1: int
    command_2: int
    data_1: int
    data_2: int
    checksum: int

    def __init__(
        self,
        *,
        address: int = DEFAULT_ADDRESS,
        command_1: int = UNSET,
        command_2: int = UNSET,
        data_1: int = UNSET,
        data_2: int = UNSET,
    ) -> None:
        validate_all_uint8(
            address,
            command_1,
            command_2,
            data_1,
            data_2,
        )
        validate_address(address)

        self.sync = SYNC
        self.address = address
        self.command_1 = command_1
        self.command_2 = command_2
        self.data_1 = data_1
        self.data_2 = data_2
        self.checksum = calculate_checksum(
            (
                address,
                command_1,
                command_2,
                data_1,
                data_2,
            )
        )

    def __iter__(self) -> Iterable[int]:
        return iter(self.as_tuple())

    def __getitem__(self, item: Union[int, slice], /) -> Union[int, Tuple[int, ...]]:
        return self.as_tuple()[item]

    def as_tuple(self) -> Tuple[int, ...]:
        return (
            self.sync,
            self.address,
            self.command_1,
            self.command_2,
            self.data_1,
            self.data_2,
            self.checksum,
        )

    def serialise(self) -> bytearray:
        return bytearray(self.as_tuple())

    @classmethod
    def deserialise(cls, command: Sequence[int], /) -> "PelcoDCommand":
        assert len(command) == D_SEND_COMMAND_LENGTH

        sync: int = command[D_COMMAND_SYNC]
        address: int = command[D_COMMAND_ADDR]
        command_1 = command[D_COMMAND_CMD1]
        command_2: int = command[D_COMMAND_CMD2]
        data_1: int = command[D_COMMAND_DATA1]
        data_2: int = command[D_COMMAND_DATA2]
        checksum: int = command[D_COMMAND_CKSM]

        assert sync == SYNC
        assert checksum == calculate_checksum(
            (
                address,
                command_1,
                command_2,
                data_1,
                data_2,
            )
        )

        return cls(
            address=address,
            command_1=command_1,
            command_2=command_2,
            data_1=data_1,
            data_2=data_2,
        )


# aka. "General Reply"
@dataclass(frozen=True, eq=True)
class GeneralResponse:
    sync: int = field(default=SYNC, repr=False)  # SYNC
    address: int = 0x00  # ADDR
    alarms: int = 0x00  # ALARMS
    checksum: int = field(default=0x00, repr=False)  # CKSM

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
    sync: int = field(default=SYNC, repr=False)  # SYNC
    address: int = 0x00  # ADDR
    response_1: int = 0x00  # RESP1
    response_2: int = 0x00  # RESP2
    data_1: int = 0x00  # DATA1
    data_2: int = 0x00  # DATA2
    checksum: int = field(default=0x00, repr=False)  # CKSM

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
    sync: int = field(default=SYNC, repr=False)  # SYNC
    address: int = 0x00  # ADDR
    data_1: int = 0x00  # DATA1
    # ...
    data_15: int = 0x00  # DATA15
    checksum: int = field(default=0x00, repr=False)  # CKSM
