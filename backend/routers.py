from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
import backend.crud as crud
import backend.schemas as schemas
from sqlalchemy.orm import Session
from backend.database import get_db

router = APIRouter()


@router.get("/")
def read_root() -> Union[str, dict]:
    return {"Hello": "World"}


@router.get("/list/", response_model=list[schemas.FoodResponse])
def list_food(database: Session = Depends(get_db), sort_by: str = "name", order: str = "asc") -> list[schemas.FoodResponse]:
    try:
        return crud.read_food_items(db=database, sort_by=sort_by, order=order)
    except ValidationError as e:
        print(e)


@router.post("/add_food/", response_model=schemas.FoodResponse, status_code=status.HTTP_201_CREATED)
def add_food(food: schemas.FoodCreate, database: Session = Depends(get_db)):
    try:
        response: schemas.FoodResponse = crud.create_food_item(
            db=database, food=food)
        return response

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@ router.put("/update_food/", response_model=schemas.FoodResponse)
def update_food(food: schemas.FoodUpdate, database: Session = Depends(get_db)):
    try:
        response: schemas.FoodResponse = crud.update_food_item(
            db=database, food=food)
        return response

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@ router.delete("/delete_food/")
def delete_food(food: schemas.FoodDelete, database: Session = Depends(get_db)):
    try:
        return crud.delete_food_item(db=database, food=food)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@ router.get("/food/{food_id}", response_model=schemas.FoodResponse)
def read_food(food_id, database: Session = Depends(get_db)):
    response: schemas.FoodResponse = crud.read_food_item(
        db=database, food_id=food_id)
    return response
