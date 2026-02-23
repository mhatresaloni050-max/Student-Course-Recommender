import requests

BASE = "http://127.0.0.1:5000"

# Test Register
resp = requests.post(f"{BASE}/register", json={
    "email": "john@example.com",
    "password": "1234"
})
try:
    print("Register:", resp.json())
except:
    print("Register raw response:", resp.text)
