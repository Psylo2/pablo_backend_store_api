import os
import bcrypt
import pytz
from datetime import datetime
from tzlocal import get_localzone
from sqlalchemy import func

from infrastructure.repositories.orm_adapter import ORMAdapter
from infrastructure.interfaces.repositories.repository_manager_interface import RepositoryManagerInterface

class RepositoryManager(RepositoryManagerInterface):

    def __init__(self):
        self.db = ORMAdapter()
        self.func = func

    @staticmethod
    def insert_timestamp() -> float:
        user_machine_timezone = pytz.timezone(get_localzone().zone)
        user_machine_timezone_localize_date = user_machine_timezone.localize(datetime.now())
        return user_machine_timezone_localize_date.astimezone(pytz.utc).timestamp()

    @staticmethod
    def convert_timestamp(timestamp: float) -> str:
        utc_timestamp = datetime.utcfromtimestamp(timestamp)
        localize_utc_timestamp = pytz.utc.localize(utc_timestamp)
        return str(localize_utc_timestamp.astimezone(pytz.timezone(get_localzone().zone)))

    @staticmethod
    def encrypt(str_field: str) -> bytes:
        key = int(os.environ.get('SALT_KEY'))
        generate_salt_key = bcrypt.gensalt(key)
        return bcrypt.hashpw(str_field.encode("UTF-8"), generate_salt_key)

    @staticmethod
    def decrypt(str_field: str, byte_field: bytes) -> bool:
        return bcrypt.checkpw(str_field.encode("UTF-8"), byte_field)


repository = RepositoryManager()
