from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..database import Base, get_db
from ..main import app


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


class CustomTestClient(TestClient):
    def delete_with_payload(self,  **kwargs):
        return self.request(method="DELETE", **kwargs)


client = CustomTestClient(app)


url = 'http://127.0.0.1:8000/'

# ** Test the add_food endpoint


def test_add_valid_without_opened_date():
    data = {
        "name": "Without_opened_date",
        "expiration_date": "2028-05-29",
        "quantity": 11,
        "opened": False
    }
    url_add = url + 'add_food/'
    response = client.post(url_add, json=data)
    response_data = response.json()

    assert response.status_code == 201

    assert isinstance(response_data['id'], int)
    assert response_data['name'] == "Without_opened_date"
    assert response_data['expiration_date'] == "2028-05-29"
    assert response_data['quantity'] == 11
    assert response_data['opened'] is False
    assert response_data['opened_date'] is None


def test_add_valid_opened_date():
    data = {
        "name": "Valid_Opened_Date",
        "expiration_date": "2028-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "2028-05-27"
    }
    url_add = url + 'add_food/'
    response = client.post(url_add, json=data)
    response_data = response.json()
    print(response_data)

    assert response.status_code == 201

    assert isinstance(response_data['id'], int)
    assert response_data['name'] == "Valid_Opened_Date"
    assert response_data['expiration_date'] == "2028-05-29"
    assert response_data['quantity'] == 11
    assert response_data['opened'] is True
    assert response_data['opened_date'] == "2028-05-27"


def test_add_invalid_empty_fields():
    datas = {
        "quantity": {
            "name": "Invalid empty fields",
            "expiration_date": "2028-05-29",
            "quantity": None,
            "opened": False
        },
        "opened": {
            "name": "Invalid empty fields",
            "expiration_date": "2028-05-29",
            "quantity": 11,
            "opened": None,
        },
        "name": {
            "name": None,
            "expiration_date": "2028-05-29",
            "quantity": 11,
            "opened": False
        },
        "expiration_date": {
            "name": "Invalid empty fields",
            "expiration_date": None,
            "quantity": 11,
            "opened": False
        }
    }
    url_add = url + 'add_food/'

    for data in datas.values():
        response = client.post(url_add, json=data)
        assert response.status_code == 422


def test_add_invalid_dates_in_past():
    data_expiration_date = {
        "name": "Past dates",
        "expiration_date": "1999-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "2028-05-28"
    }
    data_opened_date = {
        "name": "Past dates",
        "expiration_date": "2028-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "1999-05-28"
    }

    url_add = url + 'add_food/'
    response = client.post(url_add, json=data_expiration_date)
    assert response.status_code == 422
    response = client.post(url_add, json=data_opened_date)
    assert response.status_code == 422


def test_add_invalid_opened_date_missing():
    data = {
        "name": "Missing_Date",
        "expiration_date": "2030-05-29",
        "quantity": 11,
        "opened": True
    }
    url_add = url + 'add_food/'
    response = client.post(url_add, json=data)
    assert response.status_code == 422


def test_add_invalid_opened_date_not_opened():
    data = {
        "name": "Invalid_Opened_Date",
        "expiration_date": "2028-05-29",
        "quantity": 11,
        "opened": False,
        "opened_date": "2028-05-30"
    }
    url_add = url + 'add_food/'
    response = client.post(url_add, json=data)
    assert response.status_code == 422


# ** Test the list_food endpoint
def test_list_food():
    url_list = url + 'list/'
    response = client.get(url_list)
    response_data = response.json()

    assert response.status_code == 200
    assert isinstance(response_data, list)
    for food in response_data:
        assert isinstance(food['id'], int)
        assert isinstance(food['name'], str)
        assert isinstance(food['expiration_date'], str)
        assert isinstance(food['quantity'], int)
        assert isinstance(food['opened'], bool)
        if food['opened']:
            assert isinstance(food['opened_date'], str)
        else:
            assert food['opened_date'] is None


# ** Test the update_food endpoint
def test_update_valid():
    data = {
        "id": 1,
        "name": "Updated",
        "expiration_date": "2028-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "2028-05-27"
    }
    url_update = url + 'update_food/'
    response = client.put(url_update, json=data)
    response_data = response.json()

    assert response.status_code == 200

    assert response_data['id'] == 1
    assert response_data['name'] == "Updated"
    assert response_data['expiration_date'] == "2028-05-29"
    assert response_data['quantity'] == 11
    assert response_data['opened'] is True
    assert response_data['opened_date'] == "2028-05-27"


def test_update_invalid_not_opened():
    data = {
        "id": 1,
        "name": "Updated",
        "expiration_date": "2028-05-29",
        "quantity": 11,
        "opened": False,
        "opened_date": "2028-05-27"
    }
    url_update = url + 'update_food/'
    response = client.put(url_update, json=data)
    assert response.status_code == 422


# ** Test the delete_food endpoint
def test_delete_valid():
    data = {
        "id": 1
    }
    url_delete = url + 'delete_food/'
    response = client.delete_with_payload(url=url_delete, json=data)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data == {"ok": True}


def test_delete_invalid():
    data = {
        "id": 1
    }
    url_delete = url + 'delete_food/'
    response = client.delete_with_payload(url=url_delete, json=data)
    assert response.status_code == 404
