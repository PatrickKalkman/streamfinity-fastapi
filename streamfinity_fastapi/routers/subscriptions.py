from streamfinity_fastapi.db import get_session
from fastapi import APIRouter, Depends, HTTPException, Query, status
from streamfinity_fastapi.schemas.subscription_schema import Subscription
from streamfinity_fastapi.schemas.subscription_schema import SubscriptionInput
from sqlmodel import Session, select

router = APIRouter(prefix="/api/subscriptions")


@router.get("/{subscription_id}")
def get_subscription(subscription_id: int,
                     session: Session = Depends(get_session)) -> Subscription:
    subscription: Subscription | None = session.get(Subscription, subscription_id)
    if subscription:
        return subscription

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Subscription with id={subscription_id} not found")


@router.get("/")
def get_subscriptions(plan: str | None = Query(None),
                      is_active: bool | None = Query(None),
                      session: Session = Depends(get_session)) -> list[Subscription]:
    query = select(Subscription)

    if plan:
        query = query.where(Subscription.plan == plan)
    if is_active is not None:
        query = query.where(Subscription.is_active == is_active)

    return session.exec(query).all()


@router.post("/", response_model=Subscription, status_code=201)
def add_subscription(subscription_input: SubscriptionInput,
                     session: Session = Depends(get_session)) -> Subscription:
    new_subscription: Subscription = Subscription.from_orm(subscription_input)
    session.add(new_subscription)
    session.commit()
    session.refresh(new_subscription)
    return new_subscription


@router.delete("/{subscription_id}", status_code=204)
def delete_subscription(subscription_id: int,
                        session: Session = Depends(get_session)) -> None:
    subscription: Subscription | None = session.get(Subscription, subscription_id)
    if subscription:
        session.delete(subscription)
        session.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Subscription with id={subscription_id} not found")


@router.put("/{subscription_id}", response_model=Subscription)
def update_subscription(subscription_id: int, new_subscription: SubscriptionInput,
                        session: Session = Depends(get_session)) -> Subscription:
    subscription: Subscription | None = session.get(Subscription, subscription_id)
    if subscription:
        for field, value in new_subscription.dict().items():
            if value is not None:
                setattr(subscription, field, value)
        session.commit()
        return subscription
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Subscription with id={subscription_id} not found")
