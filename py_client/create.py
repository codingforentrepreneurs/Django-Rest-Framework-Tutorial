import requests

endpoint = "http://localhost:8000/api/products/" 

data = {
    "title": "This field is done",
    "price": 32.99
}
get_response = requests.post(endpoint, json=data) 
print(get_response.json())