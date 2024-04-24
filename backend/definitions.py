from enum import Enum
from backend.models import FoodItem
from sqlalchemy.sql.expression import ColumnElement  # for asc() and desc()

sortBy = {
    "name": FoodItem.name,
    "expiration_date": FoodItem.expiration_date,
    "quantity": FoodItem.quantity,
}

order = {
    "asc": ColumnElement.asc,
    "desc": ColumnElement.desc,
}
