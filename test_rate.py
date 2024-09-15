import requests
import time

BASE_URL = "http://localhost:8000"

def test_rate_limiting():
    user_id = "test_user"
    for _ in range(6):
        response = requests.post(f"{BASE_URL}/search", json={
            "text": "example query",
            "top_k": 5,
            "threshold": 0.7
        }, headers={"X-User-ID": user_id})
        if response.status_code == 429:
            print("Rate limit exceeded")
            break
        time.sleep(1)  

test_rate_limiting()
