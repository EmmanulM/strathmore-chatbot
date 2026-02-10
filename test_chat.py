import requests

url = "http://127.0.0.1:5000/chat"
data = {"message": "KCSE B+"}

response = requests.post(url, json=data)
print(response.json())
