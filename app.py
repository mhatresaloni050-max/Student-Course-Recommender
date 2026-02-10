from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import csv, os

app = Flask(__name__)
CORS(app)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["student_reco_db"]
students = db["students"]
recommendations = db["recommendations"]

# Health Check
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend running successfully"})

# REGISTER USER
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid data"}), 400

    return jsonify({"message": "Registration successful"}), 200

# LOGIN USER
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid credentials"}), 400

    return jsonify({"message": "Login successful"}), 200

# STUDENT INFO
@app.route("/student-info", methods=["POST"])
def student_info():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    required_fields = [
        "email", "full_name", "age", "grade",
        "stream", "favorite_subjects", "interests"
    ]

    for field in required_fields:
        if field not in data or str(data[field]).strip() == "":
            return jsonify({"error": f"{field} is required"}), 400

    students.update_one(
        {"email": data["email"]},
        {"$set": {
            "email": data["email"],
            "full_name": data["full_name"],
            "age": int(data["age"]),
            "grade": data["grade"],
            "stream": data["stream"],
            "favorite_subjects": data["favorite_subjects"],
            "interests": data["interests"],
            "career_goal": data.get("career_goal", "")
        }},
        upsert=True
    )

    return jsonify({"message": "Student info saved"}), 200

# SAVE PERSONALITY
@app.route("/save-personality", methods=["POST"])
def save_personality():
    data = request.get_json()
    if not data or "email" not in data or "personality" not in data:
        return jsonify({"error": "Invalid personality data"}), 400

    email = data["email"]
    personality = data["personality"]
    scores = data.get("scores", {})

    result = students.update_one(
        {"email": email},
        {"$set": {
            "personality": {
                "type": personality,
                "scores": scores
            }
        }}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Personality saved successfully"}), 200

# CAREER RECOMMENDATION
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    if not data or "email" not in data or "stream" not in data or "personality" not in data:
        return jsonify({"error": "Missing recommendation data"}), 400

    email = data["email"]
    stream = data["stream"]
    personality = data["personality"]

    careers = []
    csv_path = os.path.join(os.path.dirname(__file__), "careers.csv")

    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if (
                row["streams"].lower() == stream.lower()
                and row["required_personality"].lower() == personality.lower()
            ):
                careers.append({
                    "career": row["career"],
                    "courses": row["suggested_courses"]
                })

    # Save recommendation
    recommendations.update_one(
        {"email": email},
        {"$set": {
            "email": email,
            "careers": careers
        }},
        upsert=True
    )

    return jsonify({
        "message": "Career recommendation successful",
        "careers": careers
    }), 200

# STUDENT DASHBOARD
@app.route("/student/dashboard/<email>", methods=["GET"])
def student_dashboard(email):
    student = students.find_one({"email": email}, {"_id": 0})
    if not student:
        return jsonify({"error": "Student not found"}), 404

    rec = recommendations.find_one({"email": email}, {"_id": 0})

    return jsonify({
        "student": student,
        "personality": student.get("personality", {}),
        "careers": rec.get("careers", []) if rec else []
    }), 200

# ADMIN DASHBOARD
@app.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    total_students = students.count_documents({})

    stream_stats = list(
        students.aggregate([
            {"$group": {"_id": "$stream", "count": {"$sum": 1}}}
        ])
    )

    all_students = list(
        students.find({}, {"_id": 0, "full_name": 1, "email": 1, "stream": 1})
    )

    return jsonify({
        "total_students": total_students,
        "stream_stats": stream_stats,
        "students": all_students
    })

# RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
