from pydantic import BaseModel
from typing import Optional
from datetime import date


class FoodCreate(BaseModel):
    name: str
    expiration_date: date
    quantity: int
    opened: bool = False
    opened_date: Optional[date] = None


class FoodUpdate(BaseModel):
    id: int
    name: Optional[str]
    expiration_date: Optional[date] = None
    quantity: Optional[int] = None
    opened: Optional[bool] = None
    opened_date: Optional[date] = None


class FoodResponse(BaseModel):
    id: int
    name: str
    expiration_date: date
    quantity: int
    opened: bool
    opened_date: Optional[date] = None


class FoodDelete(BaseModel):
    id: int
