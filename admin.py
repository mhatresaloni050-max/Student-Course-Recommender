from db import students, recommendations
from flask import jsonify

def get_all_students():
    try:
        data = list(students.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_recommendations():
    try:
        data = list(recommendations.find({}, {"_id": 0}))
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
