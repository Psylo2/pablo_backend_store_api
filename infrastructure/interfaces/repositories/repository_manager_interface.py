from abc import ABC, abstractmethod


class RepositoryManagerInterface(ABC):
    db = None
    func = None

    @staticmethod
    @abstractmethod
    def convert_timestamp(timestamp: float) -> str:
        """Convert UTC TIMESTAMP to Local Host Time"""
        ...

    @staticmethod
    @abstractmethod
    def insert_timestamp() -> float:
        """Get Current time in local timezone and convert it to UTC TIMESTAMP"""
        ...

    @staticmethod
    @abstractmethod
    def decrypt(str_field: str, byte_field: bytes) -> bool:
        """Match 2 hash to Verify string context """
        ...

    @staticmethod
    @abstractmethod
    def encrypt(str_field: str) -> bytes:
        """Encrypt given string"""
        ...
