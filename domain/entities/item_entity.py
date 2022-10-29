from pydantic import BaseModel, validator


class ItemEntity(BaseModel):
    id: int | None
    title: str
    manufacturer: str
    engine_hs_power: int
    original_price: float
    on_sale: bool
    discount: int
    new_price: float
    on_stock: bool
    file_path: str
    user_id: int | None
    create_at: float | None
    last_modified: float | None

    @validator('title', 'manufacturer')
    def validate_str(cls, v) -> str:
        if not isinstance(v, str):
            raise TypeError("Type must be string")
        return v

    @validator('engine_hs_power', 'discount')
    def validate_integer(cls, v) -> int:
        if not isinstance(v, int):
            raise TypeError("Type must be integer")
        return v

    @validator('original_price', 'new_price')
    def validate_float(cls, v) -> float:
        if not isinstance(v, float):
            raise TypeError("Type must be float")
        return v

    @validator('on_sale', 'on_stock')
    def validate_bool(cls, v) -> bool:
        if not isinstance(v, bool):
            raise TypeError("Type must be bool")
        return v
