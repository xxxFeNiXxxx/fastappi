from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Movie, Genre
from schemas import *
from utils import save_image
import aiofiles
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/posters", StaticFiles(directory="posters"), name="posters")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/genres", response_model=GenreRead)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    db_genre = Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@app.get("/genres", response_model=List[GenreRead])
def get_genres(db: Session = Depends(get_db)):
    return db.query(Genre).all()

@app.post("/movies", response_model=MovieRead)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    genre_objs = db.query(Genre).filter(Genre.id.in_(movie.genres)).all()
    db_movie = Movie(**movie.dict(exclude={"genres"}))
    db_movie.genres = genre_objs
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies", response_model=List[MovieRead])
def get_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@app.get("/movies/{id}", response_model=MovieRead)
def get_movie(id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/movies/{id}", response_model=MovieRead)
def update_movie(id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    for field, value in movie.dict(exclude_unset=True, exclude={"genres"}).items():
        setattr(db_movie, field, value)
    if movie.genres:
        genre_objs = db.query(Genre).filter(Genre.id.in_(movie.genres)).all()
        db_movie.genres = genre_objs
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.put("/movies/{id}/image", response_model=MovieRead)
async def upload_movie_image(id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    image_url = await save_image(file)
    db_movie.poster_url = image_url
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movies/{id}")
def delete_movie(id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted"}
