from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from . import crud, schemas, database
from sqlalchemy.orm import Session 

router = APIRouter()
database.Base.metadata.create_all(bind=database.engine)

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
def list_food(database: Session = Depends(get_db)):
    try:
        return crud.read_food_items(db=database)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add_food/", response_model=schemas.FoodCreate)
def add_food(food: schemas.FoodCreate, database: Session = Depends(get_db)):
    try:
        return crud.create_food_item(db=database, food=food)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
