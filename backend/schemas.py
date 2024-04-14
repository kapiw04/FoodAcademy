from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date


class FoodCreate(BaseModel):
    name: str
    expiration_date: date
    quantity: int
    opened: bool = False
    opened_date: Optional[str] = None


class FoodUpdate(BaseModel):
    name: Optional[str]
    expiration_date: Optional[date]
    quantity: Optional[int]
    opened: Optional[bool] = False
    opened_date: Optional[str] = None


class FoodResponse(BaseModel):
    id: int
    name: str
    expiration_date: date
    quantity: int
    opened: bool
    opened_date: Optional[str] = None
