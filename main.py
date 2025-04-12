from typing import Union
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import random
import math

app = FastAPI(title="Store API", description="API для управления товарами", version="1.0.0")

# ---- Модели ----

class Item(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Laptop")
    price: float = Field(..., gt=0, example=999.99)
    description: Optional[str] = Field(None, max_length=500, example="A powerful laptop for work and gaming.")

# ---- Имитация базы данных ----

fake_items_db: List[Item] = []

# ---- Эндпоинты ----

@app.get("/items/", response_model=List[Item])
def get_items(
    name: Optional[str] = Query(None, min_length=2, example="phone"),
    min_price: Optional[float] = Query(None, gt=0, example=100),
    max_price: Optional[float] = Query(None, gt=0, example=1000),
    limit: int = Query(10, ge=1, le=100, example=5)
):
    items = fake_items_db
    if name:
        items = [item for item in items if name.lower() in item.name.lower()]
    if min_price:
        items = [item for item in items if item.price >= min_price]
    if max_price:
        if min_price and max_price <= min_price:
            raise HTTPException(status_code=400, detail="max_price must be greater than min_price")
        items = [item for item in items if item.price <= max_price]
    return items[:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int = Path(..., gt=0, example=42)):
    for item in fake_items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: ItemCreate = Body(...)):
    new_item = Item(id=len(fake_items_db) + 1, **item.dict())
    fake_items_db.append(new_item)
    return new_item
