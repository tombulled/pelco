from pelco.d.models import PelcoDCommand

c = PelcoDCommand(
    sync=0xFF,
    address=0x01,
    command_2=0x05,
    checksum=0x06,
)