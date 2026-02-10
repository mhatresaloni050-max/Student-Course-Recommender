import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_register():
    print("Testing /register ...")
    payload = {
        "email": "student1@gmail.com",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/register", json=payload)
    print(response.status_code, response.json())

def test_login():
    print("\nTesting /login ...")
    payload = {
        "email": "student1@gmail.com",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print(response.status_code, response.json())

def test_student_info():
    print("\nTesting /student-info ...")
    payload = {
        "email": "student1@gmail.com",
        "full_name": "Neha Patil",
        "age": 18,
        "grade": "12",
        "stream": "Science",
        "interests": ["Technology","Problem Solving"],
        "fav_subjects": ["Maths","Physics"],
        "career_goal": "Engineer"
    }
    response = requests.post(f"{BASE_URL}/student-info", json=payload)
    print(response.status_code, response.json())

def test_personality():
    print("\nTesting /personality ...")
    payload = {
        "email": "student1@gmail.com",
        "answers": [4,3,5,2,1,4,5,3,2,4,1,3,5,2,4]  # 15 answers
    }
    response = requests.post(f"{BASE_URL}/personality", json=payload)
    print(response.status_code, response.json())

def test_recommendation():
    print("\nTesting /recommend ...")
    response = requests.get(f"{BASE_URL}/recommend/student1@gmail.com")
    print(response.status_code, response.json())

def test_admin_students():
    print("\nTesting /admin/students ...")
    response = requests.get(f"{BASE_URL}/admin/students")
    print(response.status_code, response.json())

def test_admin_recommendations():
    print("\nTesting /admin/recommendations ...")
    response = requests.get(f"{BASE_URL}/admin/recommendations")
    print(response.status_code, response.json())

if __name__ == "__main__":
    test_register()
    test_login()
    test_student_info()
    test_personality()
    test_recommendation()
    test_admin_students()
    test_admin_recommendations()
