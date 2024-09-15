import requests

def test_retrieve_documents():
    url = "http://localhost:8000/search"
    payload = {
        "text": "Technology", 
        "top_k": 5,
        "threshold": 0.5
    }
    response = requests.post(url, json=payload)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

test_retrieve_documents()
