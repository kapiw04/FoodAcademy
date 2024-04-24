from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import backend.database as database
import backend.crud as crud
import backend.schemas as schemas
from sqlalchemy.orm import Session

router = APIRouter()
database.Base.metadata.create_all(bind=database.engine)


def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def read_root() -> Union[str, dict]:
    return {"Hello": "World"}


@router.get("/list/")
def list_food(database: Session = Depends(get_db), sort_by: str = "name", order: str = "asc") -> list[schemas.FoodResponse]:
    return crud.read_food_items(db=database, sort_by=sort_by, order=order)


@router.post("/add_food/", response_model=schemas.FoodResponse, status_code=status.HTTP_201_CREATED)
def add_food(food: schemas.FoodCreate, database: Session = Depends(get_db)):
    try:
        response: schemas.FoodResponse = crud.create_food_item(
            db=database, food=food)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return response


@ router.put("/update_food/", response_model=schemas.FoodUpdate)
def update_food(food: schemas.FoodUpdate, database: Session = Depends(get_db)):
    try:
        return crud.update_food_item(db=database, food=food)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@ router.delete("/delete_food/")
def delete_food(food: schemas.FoodDelete, database: Session = Depends(get_db)):
    try:
        return crud.delete_food_item(db=database, food=food)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@ router.get("/food/{food_id}", response_model=schemas.FoodResponse)
def read_food(food_id, database: Session = Depends(get_db)):
    return crud.read_food_item(db=database, food_id=food_id)
