from sqlalchemy.orm import Session
from backend.models import FoodItem
from backend.schemas import FoodCreate, FoodResponse, FoodUpdate, FoodDelete
import backend.definitions as definitions
from typing import List, Union, Dict


def create_food_item(db: Session, food: FoodCreate) -> FoodResponse:
    """Create a new food item in the database.

    Args:
        db (Session): Database session.
        food (FoodCreate): Food item to create.

    Returns:
        FoodResponse: Created food item.

    """
    new_food = FoodItem(**food.model_dump())

    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    created_food = FoodResponse(**food.model_dump(), id=new_food.id)

    return created_food


def read_food_items(db: Session, sort_by: str, order: str) -> List[FoodItem]:
    """
    Read all food items from the database.

    Args:
        db (Session): Database session.
        sort_by (str): Field to sort by.
        order (str): Order to sort by.

    Returns:
        List[FoodItem]: List of food items.

    Raises:
        ValueError: If sort_by value is invalid.
        ValueError: If order value is invalid.
    """
    if sort_by not in definitions.sortBy:
        raise ValueError(f"Invalid sort_by value: {sort_by}")

    if order not in definitions.order:
        raise ValueError(f"Invalid order value: {order}")

    order = definitions.order[order](definitions.sortBy[sort_by])

    food_items = db.query(FoodItem).order_by(order).all()
    for food in food_items:
        print(food.__dict__)

    return food_items


def read_food_item(db: Session, food_id: int) -> FoodItem:
    """
    Read a single food item from the database.

    Args:
        db (Session): Database session.
        food_id (int): Food item ID.

    Returns:
        FoodItem: Food item.
    """
    return db.query(FoodItem).filter(FoodItem.id == food_id).one_or_none()


def update_food_item(db: Session, food: FoodUpdate) -> FoodItem:
    """Update a food item in the database.

    Args:
        db (Session): Database session.
        food (FoodUpdate): Food item to update.

    Returns:
        FoodItem: Updated food item.

    Raises:
        ValueError: If food item is not found.
    """
    db_food = db.query(FoodItem).filter(
        FoodItem.id == food.id).one_or_none()

    if db_food is None:
        raise ValueError(f"Food item with ID {food.id} not found.")

    for k, v in vars(food).items():
        setattr(db_food, k, v) if v else None

    db.commit()
    db.refresh(db_food)

    return db_food


def delete_food_item(db: Session, food: FoodDelete) -> Union[Dict[str, bool], None]:
    """Delete a food item from the database.

    Args:   
        db (Session): Database session.
        food (FoodDelete): Food item to delete.

    Returns:
        Dict[str, bool]: Deletion status.

    Raises:
        ValueError: If food item is not found.
    """

    db_food = db.query(FoodItem).filter(
        FoodItem.id == food.id).one_or_none()

    if db_food is None:
        raise ValueError(f"Food item with ID {food.id} not found.")

    db.delete(db_food)
    db.commit()

    return {
        "ok": True,
    }
