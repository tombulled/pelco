import pytest

from pelcod.errors import ValidationError
from pelcod.models import PelcoDCommand


@pytest.fixture
def command() -> PelcoDCommand:
    return PelcoDCommand(
        address=0x01,
        command_2=0x05,
    )


def test_PelcoDCommand_as_tuple(command: PelcoDCommand) -> None:
    assert command.as_tuple() == (0xFF, 0x01, 0x00, 0x05, 0x00, 0x00, 0x06)


def test_PelcoDCommand_serialise(command: PelcoDCommand) -> None:
    assert command.serialise() == bytearray(b"\xff\x01\x00\x05\x00\x00\x06")


def test_PelcoDCommand_deserialise(command: PelcoDCommand) -> None:
    assert PelcoDCommand.deserialise(b"\xff\x01\x00\x05\x00\x00\x06") == command


def test_PelcoDCommand_init() -> None:
    with pytest.raises(ValidationError):
        PelcoDCommand(command_1=0xFF + 1)
