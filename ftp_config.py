from dataclasses import dataclass
from enum import Enum

class FTPMode(Enum):
    ACTIVE = "active"
    PASSIVE = "passive"

class TransferMode(Enum):
    ASCII = "A"
    BINARY = "I"

@dataclass
class FTPConfig:
    host: str = '127.0.0.1'
    port: int = 21
    clamav_host: str = '127.0.0.1'
    clamav_port: int = 9999
    username: str = 'mduy'
    password: str = '142857'
    use_ssl: bool = True
    buffer_size: int = 4096
    timeout: int = 20
    mode: FTPMode = FTPMode.ACTIVE
    transfer_mode: TransferMode = TransferMode.ASCII
    is_quit: bool = False

ftpconfig = FTPConfig()