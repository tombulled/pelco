from typing import NamedTuple


class PelcoDCommand(NamedTuple):
    sync: int = 0
    address: int = 0
    command: int = 0
    data: int = 0
    checksum: int = 0

    def __init__(self, sync: int):
        assert sync < 5

        self.sync = sync