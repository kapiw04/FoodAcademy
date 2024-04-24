import requests

url = 'http://127.0.0.1:8000/'

# ** Test the add_food endpoint


def test_add_valid_without_opened_date():
    data = {
        "name": "Orange",
        "expiration_date": "2024-05-29",
        "quantity": 11,
        "opened": False
    }
    url_add = url + 'add_food/'
    response = requests.post(url_add, json=data)
    response_data = response.json()

    assert response.status_code == 201

    assert isinstance(response_data['id'], int)
    assert response_data['name'] == "Orange"
    assert response_data['expiration_date'] == "2024-05-29"
    assert response_data['quantity'] == 11
    assert response_data['opened'] is False
    assert response_data['opened_date'] is None


def test_add_valid_opened_date():
    data = {
        "name": "Orange",
        "expiration_date": "2024-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "2024-05-30"
    }
    url_add = url + 'add_food/'
    response = requests.post(url_add, json=data)
    response_data = response.json()
    print(response_data)

    assert response.status_code == 201

    assert isinstance(response_data['id'], int)
    assert response_data['name'] == "Orange"
    assert response_data['expiration_date'] == "2024-05-29"
    assert response_data['quantity'] == 11
    assert response_data['opened'] is True
    assert response_data['opened_date'] == "2024-05-30"


def test_add_invalid_empty_fields():
    datas = {
        "quantity": {
            "name": "Orange",
            "expiration_date": "2024-05-29",
            "quantity": None,
            "opened": False
        },
        "opened": {
            "name": "Orange",
            "expiration_date": "2024-05-29",
            "quantity": 11,
            "opened": None,
        },
        "name": {
            "name": None,
            "expiration_date": "2024-05-29",
            "quantity": 11,
            "opened": False
        },
        "expiration_date": {
            "name": "Orange",
            "expiration_date": None,
            "quantity": 11,
            "opened": False
        }
    }
    url_add = url + 'add_food/'

    for data in datas.values():
        response = requests.post(url_add, json=data)
        assert response.status_code == 422


def test_add_invalid_dates_in_past():
    data_expiration_date = {
        "name": "Orange",
        "expiration_date": "1999-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "2024-05-28"
    }
    data_opened_date = {
        "name": "Orange",
        "expiration_date": "2024-05-29",
        "quantity": 11,
        "opened": True,
        "opened_date": "1999-05-28"
    }

    url_add = url + 'add_food/'
    response = requests.post(url_add, json=data_expiration_date)
    assert response.status_code == 422
    response = requests.post(url_add, json=data_opened_date)
    assert response.status_code == 422


def test_add_invalid_opened_date_missing():
    data = {
        "name": "Orange",
        "expiration_date": "2024-05-29",
        "quantity": 11,
        "opened": True
    }
    url_add = url + 'add_food/'
    response = requests.post(url_add, json=data)
    assert response.status_code == 422


def test_add_invalid_opened_date_not_opened():
    data = {
        "name": "Orange",
        "expiration_date": "2024-05-29",
        "quantity": 11,
        "opened": False,
        "opened_date": "2024-05-30"
    }
    url_add = url + 'add_food/'
    response = requests.post(url_add, json=data)
    assert response.status_code == 422
