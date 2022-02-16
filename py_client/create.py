import requests


headers = {'Authorization': 'Bearer 56be721aeecb0ed611e2765e9253e2d62f0badfc'}
endpoint = "http://localhost:8000/api/products/" 

data = {
    "title": "This field is done",
    "price": 32.99
}
get_response = requests.post(endpoint, json=data, headers=headers) 
print(get_response.json())