from pydantic import BaseModel, validator


class UserEntity(BaseModel):
    id: int | None
    name: str
    email: bytes
    password: bytes
    create_at:  float | None
    last_login: float | None

    @validator('name')
    def validate_str(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError("Type must be string")
        return v

    @validator('email')
    def validate_bytes(cls, v) -> bytes:
        if not isinstance(v, bytes):
            raise TypeError("Type must be bytes")
        return v

    @validator('create_at', 'last_login')
    def validate_float(cls, v) -> float:
        if not isinstance(v, float):
            raise TypeError("Type must be float")
        return v
