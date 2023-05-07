from sqlmodel import SQLModel, Field


class UserInput(SQLModel):
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool = True


class User(UserInput, table=True):
    id: int = Field(default=None, primary_key=True)
