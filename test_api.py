# test_api_endpoints.py
import requests

BASE_URL = "http://localhost:8000"

def test_search_endpoint():
    response = requests.post(f"{BASE_URL}/search", json={
        "text": "example query",
        "top_k": 5,
        "threshold": 0.7
    })
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'results' in response.json(), "Response does not contain 'results' key"

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

test_search_endpoint()
test_health_endpoint()
