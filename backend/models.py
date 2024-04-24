from sqlalchemy import Column, Integer, String, Boolean, Date
from backend.database import Base


class FoodItem(Base):
    __tablename__ = 'food_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    expiration_date = Column(Date)
    quantity = Column(Integer)
    opened = Column(Boolean, default=False)
    opened_date = Column(Date, nullable=True)
