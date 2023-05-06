from datetime import date

from sqlmodel import Relationship, SQLModel, Field


class ActorInput(SQLModel):
    first_name: str
    last_name: str
    date_of_birth: date
    nationality: str
    biography: str | None = None
    profile_picture_url: str | None = None


class MovieInput(SQLModel):
    title: str
    length: int
    synopsis: str
    release_year: int
    director: str
    genre: str
    rating: int | None = None

    class Config:
        schema_extra = {
            "example": {
                "title": "The Matrix",
                "length": 136,
                "synopsis": "A computer hacker learns from mysterious rebels",
                "release_year": 1999,
                "director": "Lana Wachowski, Lilly Wachowski",
                "genre": "Action, Sci-Fi",
                "rating": 8,
            }
        }


class MovieActorLink(SQLModel, table=True):
    movie_id: int = Field(foreign_key="movie.id", primary_key=True, default=None)
    actor_id: int = Field(foreign_key="actor.id", primary_key=True, default=None)


class Movie(MovieInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    actors: list["Actor"] = Relationship(back_populates="movies",
                                         link_model=MovieActorLink)


class Actor(ActorInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    movies: list["Movie"] = Relationship(back_populates="actors",
                                         link_model=MovieActorLink)


class MovieOutput(MovieInput):
    id: int
    actors: list["ActorOutput"]


class ActorOutput(ActorInput):
    id: int
    movies: list[MovieOutput]
