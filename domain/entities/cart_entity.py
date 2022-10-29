from pydantic import BaseModel, validator


class CartEntity(BaseModel):
    id: int | None
    items: list
    user_id: int
    create_at: float | None
    last_modified: float | None

    @validator('items')
    def validate_str(cls, v) -> list:
        if not isinstance(v, list):
            raise TypeError("Type must be List")
        return v

    @validator('user_id')
    def validate_integer(cls, v) -> int:
        if not isinstance(v, int):
            raise TypeError("Type must be integer")
        return v
