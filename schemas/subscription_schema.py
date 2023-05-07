from datetime import date

from sqlmodel import Field, SQLModel


class SubscriptionInput(SQLModel):
    user_id: int
    plan: str
    start_date: date
    end_date: date | None = None
    is_active: bool = True


class Subscription(SubscriptionInput, table=True):
    id: int = Field(default=None, primary_key=True)
