from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from db import get_session

from schemas.movie_actor_schema import MovieInput, Movie


router = APIRouter(prefix="/api/movies")


@router.get("/")
def get_movies(release_year: int | None = None,
               session: Session = Depends(get_session)) -> list[Movie]:
    query = select(Movie)
    if release_year:
        query = query.where(Movie.release_year == release_year)
    return session.exec(query).all()


@router.get("/{movie_id}")
def get_movie(movie_id: int,
              session: Session = Depends(get_session)) -> Movie:
    movie: Movie | None = session.get(Movie, movie_id)
    if movie:
        return movie

    raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found")


@router.post("/", response_model=Movie)
def add_movie(movie_input: MovieInput,
              session: Session = Depends(get_session)) -> Movie:
    new_movie: Movie = Movie.from_orm(movie_input)
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)
    return new_movie


@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int,
                 session: Session = Depends(get_session)) -> None:
    movie: Movie | None = session.get(Movie, movie_id)
    if movie:
        session.delete(movie)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found")


@router.put("/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, new_movie: MovieInput,
                 session: Session = Depends(get_session)) -> Movie:
    movie: Movie | None = session.get(Movie, movie_id)
    if movie:
        # update movie from database with values from new_movie
        for field, value in new_movie.dict().items():
            if value is not None:
                setattr(movie, field, value)
        session.commit()
        return movie
    else:
        raise HTTPException(status_code=404, detail=f"Movie with id={movie_id} not found")
