from flask import request, jsonify
from db import students, personality_tests

# Save student info
def save_student_info():
    try:
        data = request.json
        required_fields = ["email", "full_name", "age", "grade", "stream",
                           "interests", "fav_subjects", "career_goal"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400

        students.update_one(
            {"email": data["email"]},
            {"$set": data},
            upsert=True
        )

        return jsonify({"message": "Student info saved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Save personality test
def save_personality():
    try:
        data = request.json
        email = data.get("email")
        answers = data.get("answers")  # list of 15 integers 1-5

        if not email or not answers or len(answers) != 15:
            return jsonify({"error": "Email and 15 answers required"}), 400

        # Simple personality scoring
        scores = {
            "analytical": answers[0] + answers[3] + answers[6] + answers[9],
            "creative": answers[1] + answers[4] + answers[7] + answers[10],
            "leadership": answers[2] + answers[5] + answers[8] + answers[11],
            "social": answers[12] + answers[13] + answers[14]
        }

        personality_tests.update_one(
            {"email": email},
            {"$set": {"answers": answers, "scores": scores}},
            upsert=True
        )

        return jsonify({"message": "Personality test saved", "scores": scores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
