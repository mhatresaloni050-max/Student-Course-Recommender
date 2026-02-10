from flask import request, jsonify
import bcrypt
from db import users

def register():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        if users.find_one({"email": email}):
            return jsonify({"error": "User already exists"}), 400

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        users.insert_one({
            "email": email,
            "password": hashed,
            "role": "student"
        })

        return jsonify({"message": "Registration successful"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        user = users.find_one({"email": email})
        if user and bcrypt.checkpw(password.encode(), user["password"]):
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
