from database import SessionLocal
from models import Genre, Movie
from datetime import datetime

def seed():
    db = SessionLocal()

    # Жанры
    action = db.query(Genre).filter_by(name="Action").first()
    if not action:
        action = Genre(name="Action", description="Action-packed films")
        db.add(action)
        db.commit()
        db.refresh(action)

    drama = db.query(Genre).filter_by(name="Drama").first()
    if not drama:
        drama = Genre(name="Drama", description="Dramatic films")
        db.add(drama)
        db.commit()
        db.refresh(drama)

    # Фильмы
    if db.query(Movie).count() == 0:
        movie1 = Movie(
            title="Inception",
            year=2010,
            duration=148,
            rating=8.8,
            description="A mind-bending thriller",
            genres=[action],
            created_at=datetime.utcnow()
        )
        movie2 = Movie(
            title="The Shawshank Redemption",
            year=1994,
            duration=142,
            rating=9.3,
            description="Hope is a dangerous thing.",
            genres=[drama],
            created_at=datetime.utcnow()
        )
        db.add_all([movie1, movie2])
        db.commit()

    db.close()

if __name__ == "__main__":
    seed()
