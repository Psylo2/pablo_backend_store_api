from pydantic import BaseModel, validator


class PasswordEntity(BaseModel):
    id: int | None
    username: str
    current_password: bytes
    last_change: float  | None
    password_last_1:  bytes | None
    password_last_2: bytes | None
    password_last_3: bytes | None
    password_last_4: bytes | None
    password_last_5: bytes | None
    password_last_6: bytes | None
    password_last_7: bytes | None
    password_last_8: bytes | None
    password_last_9: bytes | None
    password_last_10: bytes | None

    @validator('username')
    def validate_str(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError("Type must be string")
        return v

    @validator('current_password')
    def validate_bytes(cls, v) -> bytes:
        if not isinstance(v, bytes):
            raise TypeError("Type must be bytes")
        return v
