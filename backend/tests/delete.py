import requests
import sys

id = sys.argv[1]

url = 'http://127.0.0.1:8000/delete_food/'
data = {
    "id": id
}

response = requests.delete(url, json=data)
print(response.status_code)
print(response.json())
