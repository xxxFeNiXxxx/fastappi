from typing import Union
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import random
import math

app = FastAPI()

# Модель для ответа на /about
class DeveloperInfo(BaseModel):
    full_name: str
    group: str
    project: str

@app.get("/about", response_model=DeveloperInfo)
def get_about():
    return DeveloperInfo(
        full_name="Иванов Иван Иванович",
        group="Группа БИВТ-21",
        project="Проект: Геометрическое API"
    )

@app.get("/rnd")
def get_random_number():
    return {"random_number": random.randint(1, 10)}

@app.post("/t_square")
def calculate_triangle(
    a: float = Query(..., gt=0, description="Сторона a (> 0)"),
    b: float = Query(..., gt=0, description="Сторона b (> 0)"),
    c: float = Query(..., gt=0, description="Сторона c (> 0)")
):
    # Проверка на возможность существования треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        raise HTTPException(status_code=400, detail="Треугольник с такими сторонами не существует")

    perimeter = a + b + c
    s = perimeter / 2  # Полупериметр
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))

    return {
        "perimeter": perimeter,
        "area": area
    }
