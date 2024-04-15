import requests
import pytest

BASE_URL = "http://127.0.0.1:8000"  # Adjust this to your API's URL

# Tests for GET at the root endpoint


def test_get_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    # Adjust based on expected response
    assert isinstance(response.json(), (str, dict))

# Tests for GET at the /list/ endpoint


def test_list_food_default():
    response = requests.get(f"{BASE_URL}/list/")
    assert response.status_code == 200


def test_list_food_sort_order():
    response = requests.get(f"{BASE_URL}/list/",
                            params={"sort_by": "name", "order": "asc"})
    assert response.status_code == 200


def test_list_food_validation_error():
    response = requests.get(
        f"{BASE_URL}/list/", params={"sort_by": "invalid_sort", "order": "invalid_order"})
    assert response.status_code == 422

# Tests for POST at the /add_food/ endpoint


def test_add_food():
    food_data = {"name": "Apple",
                 "expiration_date": "2024-12-31", "quantity": 10}
    response = requests.post(f"{BASE_URL}/add_food/", json=food_data)
    assert response.status_code == 200
    assert response.json().get("name") == "Apple"


def test_add_food_validation_error():
    food_data = {"name": ""}  # Missing required fields
    response = requests.post(f"{BASE_URL}/add_food/", json=food_data)
    assert response.status_code == 422

# Tests for PUT at the /update_food/ endpoint


def test_update_food():
    update_data = {"id": 1, "name": "Updated Apple", "quantity": 15}
    response = requests.put(f"{BASE_URL}/update_food/", json=update_data)
    assert response.status_code == 200
    assert response.json().get("name") == "Updated Apple"


def test_update_food_validation_error():
    update_data = {"id": 999}  # Assuming 999 does not exist
    response = requests.put(f"{BASE_URL}/update_food/", json=update_data)
    assert response.status_code == 422

# Tests for DELETE at the /delete_food/ endpoint


def test_delete_food():
    response = requests.delete(f"{BASE_URL}/delete_food/", json={"id": 1})
    assert response.status_code == 200


def test_delete_food_validation_error():
    response = requests.delete(f"{BASE_URL}/delete_food/", json={"id": 999})
    assert response.status_code == 422
