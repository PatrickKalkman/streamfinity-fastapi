from datetime import date, timedelta
from streamfinity_fastapi.schemas.subscription_schema import SubscriptionInput
from streamfinity_fastapi.streamfinity import app
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)

# Test data
test_subscription = SubscriptionInput(
    user_id=1,
    plan="Basic",
    start_date=date.today(),
    end_date=date.today() + timedelta(days=30),
    is_active=True,
)


def get_test_subscription_json():
    assert test_subscription.end_date is not None
    json = {
      **test_subscription.dict(),
      "start_date": test_subscription.start_date.isoformat(),
      "end_date": test_subscription.end_date.isoformat(),
    }
    return json


def create_subscription():
    json = get_test_subscription_json()
    response = client.post("/api/subscriptions/", json=json)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["id"]


def test_create_subscription():
    json = get_test_subscription_json()
    response = client.post("/api/subscriptions/", json=json)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_id"] == test_subscription.user_id
    assert response.json()["plan"] == test_subscription.plan


def test_get_subscription():
    subscription_id = create_subscription()
    response = client.get(f"/api/subscriptions/{subscription_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["user_id"] == test_subscription.user_id
    assert response.json()["plan"] == test_subscription.plan


def test_get_subscriptions():
    response = client.get("/api/subscriptions/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_update_subscription():
    subscription_id = create_subscription()
    updated_subscription = test_subscription.copy(
        update={"plan": "Premium"}
    ).dict()
    updated_subscription["start_date"] = updated_subscription["start_date"].isoformat()
    updated_subscription["end_date"] = updated_subscription["end_date"].isoformat()
    response = client.put(
        f"/api/subscriptions/{subscription_id}", json=updated_subscription
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["plan"] == "Premium"


def test_delete_subscription():
    subscription_id = create_subscription()
    response = client.delete(f"/api/subscriptions/{subscription_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
