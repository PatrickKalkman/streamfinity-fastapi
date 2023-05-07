from datetime import date

from fastapi import Depends, HTTPException, APIRouter, Query
from sqlmodel import Session, select
from db import get_session

from schemas.movie_actor_schema import Actor, ActorInput


router = APIRouter(prefix="/api/actors")


@router.get("/{actor_id}")
def get_actor(actor_id: int,
              session: Session = Depends(get_session)) -> Actor:
    actor: Actor | None = session.get(Actor, actor_id)
    if actor:
        return actor

    raise HTTPException(status_code=404, detail=f"Actor with id={actor_id} not found")


@router.get("/")
def get_actors(name: str | None = Query(None),
               birthdate: date | None = Query(None),
               nationality: str | None = Query(None),
               session: Session = Depends(get_session)) -> list[Actor]:

    query = select(Actor)

    if name:
        query = query.where(Actor.last_name == name)
    if birthdate:
        query = query.where(Actor.date_of_birth == birthdate)
    if nationality:
        query = query.where(Actor.nationality == nationality)

    return session.exec(query).all()


@router.post("/", response_model=Actor, status_code=201)
def add_actor(actor_input: ActorInput,
              session: Session = Depends(get_session)) -> Actor:
    new_actor: Actor = Actor.from_orm(actor_input)
    session.add(new_actor)
    session.commit()
    session.refresh(new_actor)
    return new_actor


@router.delete("/{actor_id}", status_code=204)
def delete_actor(actor_id: int,
                 session: Session = Depends(get_session)) -> None:
    actor: Actor | None = session.get(Actor, actor_id)
    if actor:
        session.delete(actor)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Actor with id={actor_id} not found")


@router.put("/{actor_id}", response_model=Actor)
def update_actor(actor_id: int, new_actor: ActorInput,
                 session: Session = Depends(get_session)) -> Actor:
    actor: Actor | None = session.get(Actor, actor_id)
    if actor:
        for field, value in new_actor.dict().items():
            if value is not None:
                setattr(actor, field, value)
        session.commit()
        return actor
    else:
        raise HTTPException(status_code=404, detail=f"Actor with id={actor_id} not found")
