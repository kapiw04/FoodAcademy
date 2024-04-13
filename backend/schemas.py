from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date


class FoodCreate(BaseModel):
    name: str
    expiration_date: str
    quantity: int
    opened: bool = False
    opened_date: Optional[str] = None

class FoodResponse(BaseModel):
    id: int
    name: str
    expiration_date: str
    quantity: int
    opened: bool
    opened_date: Optional[str] = None

    @field_validator('expiration_date')
    @classmethod
    def format_expiration_date(cls, value):
        if isinstance(value, date):
            return value.strftime("%d-%m-%Y")
        return value