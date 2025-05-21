from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int
    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    duration: Optional[int] = Field(None, gt=0)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None
    genres: List[int] = []

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

class MovieRead(MovieBase):
    id: int
    poster_url: Optional[HttpUrl]
    created_at: datetime
    genres: List[GenreRead]
    class Config:
        orm_mode = True
