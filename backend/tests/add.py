import requests
from datetime import date

url = 'http://127.0.0.1:8000/add_food/'
data = {
    "name": "Orange",
    "expiration_date": date(2024, 5, 29).isoformat(),
    "quantity": 11,
    "opened": False
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
