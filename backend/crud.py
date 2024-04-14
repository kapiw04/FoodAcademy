from sqlalchemy.orm import Session
from . import models, schemas


def create_food_item(db: Session, food: schemas.FoodCreate):
    new_food = models.FoodItem(**food.model_dump())

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    created_food = schemas.FoodResponse(**food.model_dump(), id=new_food.id)

    return created_food


def read_food_items(db: Session):
    return db.query(models.FoodItem).all()


def update_food_item(db: Session, food: schemas.FoodUpdate):
    db_food = db.query(models.FoodItem).filter(
        models.FoodItem.id == food.id).one_or_none()

    if db_food is None:
        return None

    for k, v in vars(food).items():
        setattr(db_food, k, v) if v else None

    db.commit()
    db.refresh(db_food)

    return db_food


def delete_food_item(db: Session, food: schemas.FoodDelete):
    db_food = db.query(models.FoodItem).filter(
        models.FoodItem.id == food.id).one_or_none()

    if db_food is None:
        return None

    db.delete(db_food)
    db.commit()

    return {
        "ok": True,
    }
