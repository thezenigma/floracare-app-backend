import requests
response = requests.post('http://localhost:8000/api/plants/search', json={'query': 'Gray Dragon'})
print("Status:", response.status_code)
print("Response:", response.json())
