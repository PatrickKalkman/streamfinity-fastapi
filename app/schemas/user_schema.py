from sqlmodel import Field, SQLModel


class UserInput(SQLModel):
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True


class User(UserInput, table=True):
    id: int = Field(default=None, primary_key=True)
