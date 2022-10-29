from pydantic import BaseModel, validator


class PaymentEntity(BaseModel):
    id: int | None
    amount: int
    total_quantity: int
    user_id: int
    payment_at: float | None
    state: str
    transaction_id: str | None
    refund_at: float | None
    items: list

    @validator('items')
    def validate_list(cls, v) -> list:
        if not isinstance(v, list):
            raise TypeError("Type must be list")
        return v

    @validator('total_quantity', 'user_id', 'amount')
    def validate_integer(cls, v) -> int:
        if not isinstance(v, int):
            raise TypeError("Type must be integer")
        return v
