from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def create_food_item(db: Session, food: schemas.FoodCreate):
    food.model_dump()

    new_food = models.FoodItem(**food.model_dump())

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    created_food = schemas.FoodResponse(**food.model_dump(), id=new_food.id)

    return created_food


def read_food_items(db: Session):
    return db.query(models.FoodItem).all()


def update_food_item(db: Session, food: schemas.FoodUpdate):
    new_food = models.FoodItem(
        name=food.name,
        expiration_date=datetime.strptime(food.expiration_date, "%d-%m-%Y"),
        quantity=food.quantity,
        opened=food.opened,
        opened_date=datetime.strptime(
            food.opened_date, "%d-%m-%Y") if food.opened_date else None
    )

    created_food = schemas.FoodResponse(
        id=new_food.id,
        name=new_food.name,
        expiration_date=new_food.expiration_date.strftime("%d-%m-%Y"),
        quantity=new_food.quantity,
        opened=new_food.opened,
        opened_date=new_food.opened_date.strftime(
            "%d-%m-%Y") if new_food.opened_date else None
    )

    return created_food
