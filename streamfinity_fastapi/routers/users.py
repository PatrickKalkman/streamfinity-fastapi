from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from streamfinity_fastapi.db import get_session
from streamfinity_fastapi.schemas.user_schema import User, UserInput
from streamfinity_fastapi.security.hashing import get_password_hash

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    user: User | None = session.get(User, user_id)
    if user:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with id={user_id} not found")


@router.get("/")
def get_users(email: str | None = Query(None),
              session: Session = Depends(get_session)) -> list[User]:
    query = select(User)

    if email:
        query = query.where(User.email == email)

    return session.exec(query).all()


@router.post("/", response_model=User, status_code=201)
def add_user(user_input: UserInput, session: Session = Depends(get_session)) -> User:
    hashed_password = get_password_hash(user_input.password)
    user_input.password = hashed_password

    new_user: User = User.from_orm(user_input)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_session)) -> None:
    user: User | None = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={user_id} not found")


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, new_user: UserInput,
                session: Session = Depends(get_session)) -> User:
    user: User | None = session.get(User, user_id)
    if user:
        for field, value in new_user.dict().items():
            if value is not None:
                setattr(user, field, value)
        session.commit()
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User with id={user_id} not found")
