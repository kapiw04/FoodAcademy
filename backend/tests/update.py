import requests

url = 'http://127.0.0.1:8000/update_food/'
data = {
    "id": 1,
    "name": "Orange",
}

response = requests.put(url, json=data)
print(response.status_code)
print(response.json())
