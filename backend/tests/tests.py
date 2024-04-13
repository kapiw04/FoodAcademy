import requests

url = 'http://127.0.0.1:8000/add_food/'
data = {
    "name": "Apple",
    "expiration_date": "27-05-2024",
    "quantity": 10,
    "opened": False
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
