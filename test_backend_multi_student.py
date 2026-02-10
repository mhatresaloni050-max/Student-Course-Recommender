import requests

BASE_URL = "http://127.0.0.1:5000"

students = [
    {
        "email": "science_student@gmail.com",
        "password": "123456",
        "info": {
            "full_name": "Amit Sharma",
            "age": 18,
            "grade": "12",
            "stream": "Science",
            "interests": ["Technology", "Problem Solving"],
            "fav_subjects": ["Maths", "Physics"],
            "career_goal": "Engineer"
        },
        "personality": [5,4,5,4,3,5,4,4,3,5,4,4,5,3,4]
    },
    {
        "email": "commerce_student@gmail.com",
        "password": "123456",
        "info": {
            "full_name": "Neha Patil",
            "age": 17,
            "grade": "11",
            "stream": "Commerce",
            "interests": ["Finance", "Business"],
            "fav_subjects": ["Accounts", "Economics"],
            "career_goal": "Business Analyst"
        },
        "personality": [4,5,4,4,4,3,5,4,4,3,5,4,4,3,4]
    },
    {
        "email": "arts_student@gmail.com",
        "password": "123456",
        "info": {
            "full_name": "Riya Deshmukh",
            "age": 18,
            "grade": "12",
            "stream": "Arts",
            "interests": ["Design", "Creativity"],
            "fav_subjects": ["Psychology", "Drawing"],
            "career_goal": "Designer"
        },
        "personality": [3,4,3,5,5,3,4,5,4,3,5,4,5,3,4]
    }
]

def register(student):
    print(f"\nRegistering {student['email']}")
    res = requests.post(f"{BASE_URL}/register", json={
        "email": student["email"],
        "password": student["password"]
    })
    print(res.status_code, res.json())

def login(student):
    print(f"Logging in {student['email']}")
    res = requests.post(f"{BASE_URL}/login", json={
        "email": student["email"],
        "password": student["password"]
    })
    print(res.status_code, res.json())

def student_info(student):
    print("Submitting student info")
    data = student["info"]
    data["email"] = student["email"]
    res = requests.post(f"{BASE_URL}/student-info", json=data)
    print(res.status_code, res.json())

def personality_test(student):
    print("Submitting personality test")
    res = requests.post(f"{BASE_URL}/personality", json={
        "email": student["email"],
        "answers": student["personality"]
    })
    print(res.status_code, res.json())

def recommendation(student):
    print("Fetching recommendation")
    res = requests.get(f"{BASE_URL}/recommend/{student['email']}")
    print(res.status_code, res.json())

def admin_checks():
    print("\nAdmin: Fetching all students")
    print(requests.get(f"{BASE_URL}/admin/students").json())

    print("\nAdmin: Fetching all recommendations")
    print(requests.get(f"{BASE_URL}/admin/recommendations").json())

if __name__ == "__main__":
    for s in students:
        register(s)
        login(s)
        student_info(s)
        personality_test(s)
        recommendation(s)

    admin_checks()
