import requests
from datetime import date

url = 'http://127.0.0.1:8000/add_food/'
data = {
    "name": "Apple",
    "expiration_date": date(2024, 5, 27).isoformat(),
    "quantity": 10,
    "opened": False
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
