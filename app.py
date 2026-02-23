from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import traceback
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv


app = Flask(__name__)
CORS(app)

DB_PATH = "student_reco.db"

# ---------------- ADMIN ----------------
load_dotenv()

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
# ---------------- HELPERS ----------------
def normalize(text):
    return text.strip().lower() if text else ""

# ---------------- DATABASE ----------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        age INTEGER,
        grade TEXT,
        stream TEXT,
        interests TEXT,
        career_goal TEXT,
        personality_type TEXT,
        personality_scores TEXT,
        budget INTEGER DEFAULT 0,
        course_type TEXT DEFAULT 'full-time'
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        careers TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- CSV LOADING ----------------
data = pd.read_csv("Careers_Dataset.csv")
feature_cols = ["Hobby", "Personality", "Career_Goal", "Stream"]

for col in feature_cols:
    if col not in data.columns:
        data[col] = "unknown"
    data[col] = data[col].fillna("unknown").astype(str).str.strip().str.lower()

if "Average_Fees" not in data.columns:
    data["Average_Fees"] = 0
else:
    data["Average_Fees"] = pd.to_numeric(data["Average_Fees"], errors='coerce').fillna(0)

if "Course_Type" not in data.columns:
    data["Course_Type"] = "full-time"
else:
    data["Course_Type"] = data["Course_Type"].fillna("full-time").astype(str).str.strip().str.lower()

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return jsonify({"status":"Backend running"})

@app.route("/register", methods=["POST"])
def register():
    data_in = request.get_json()
    if not data_in:
        return jsonify({"error":"No data"}), 400
    email = normalize(data_in.get("email",""))
    password = data_in.get("password","").strip()
    full_name = data_in.get("full_name","")
    if not email or not password:
        return jsonify({"error":"Missing email or password"}),400
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO students (email,password,full_name) VALUES (?,?,?)",
                     (email,password,full_name))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error":"User exists"}),409
    conn.close()
    return jsonify({"message":"Registration successful"})

@app.route("/login", methods=["POST"])
def login():
    data_in = request.get_json()
    email = normalize(data_in.get("email",""))
    password = data_in.get("password","").strip()
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM students WHERE email=? AND password=?",
        (email,password)
    ).fetchone()
    conn.close()
    if user:
        return jsonify({"message":"Login successful"}),200
    return jsonify({"message":"Invalid credentials"}),401

@app.route("/admin/login", methods=["POST"])
def admin_login():
    data_in = request.get_json()
    if not data_in:
        return jsonify({"error": "No data provided"}), 400

    email = normalize(data_in.get("email",""))
    password = data_in.get("password","").strip()

    if email == normalize(ADMIN_EMAIL) and password == ADMIN_PASSWORD:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/admin-check", methods=["GET"])
def admin_check():
    # For now, just return success; later you can verify token/session
    return jsonify({"message": "Admin verified"})

@app.route("/admin/students", methods=["GET"])
def admin_get_students():
    try:
        conn = get_db_connection()
        students = conn.execute("SELECT full_name, email, stream FROM students").fetchall()
        conn.close()
        student_list = [dict(s) for s in students]
        return jsonify(student_list)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/student-info", methods=["POST"])
def student_info():
    data_in = request.get_json()
    if not data_in or "email" not in data_in:
        return jsonify({"error":"No data"}),400
    email = normalize(data_in["email"])
    conn = get_db_connection()
    conn.execute("""
        UPDATE students SET
            full_name=?, age=?, grade=?, stream=?, 
            interests=?, career_goal=?, budget=?, course_type=?
        WHERE email=?
    """, (
        data_in.get("full_name",""),
        data_in.get("age"),
        data_in.get("grade"),
        data_in.get("stream"),
        data_in.get("interests"),
        data_in.get("career_goal",""),
        data_in.get("budget",0),
        data_in.get("course_type","full-time"),
        email
    ))
    conn.commit()
    conn.close()
    return jsonify({"message":"Student info saved"})

@app.route("/save-personality", methods=["POST"])
def save_personality():
    try:
        data_in = request.get_json()
        if not data_in or "email" not in data_in:
            return jsonify({"error": "Missing email"}), 400
        email = normalize(data_in["email"])
        personality = normalize(data_in.get("personality",""))
        scores = data_in.get("scores", {})
        if not personality:
            return jsonify({"error": "Personality type cannot be empty"}), 400
        if not isinstance(scores, dict):
            return jsonify({"error": "Scores must be a JSON object"}), 400
        conn = get_db_connection()
        exists = conn.execute("SELECT 1 FROM students WHERE email=?", (email,)).fetchone()
        if not exists:
            conn.close()
            return jsonify({"error": "Student not found"}), 404
        conn.execute("""
            UPDATE students SET personality_type=?, personality_scores=? WHERE email=?
        """, (personality, json.dumps(scores), email))
        conn.commit()
        conn.close()
        return jsonify({"message":"Personality saved successfully"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}),500

# ---------------- RECOMMEND ----------------
@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        user_input = request.json or {}

        email = normalize(user_input.get("email", ""))
        hobby = normalize(user_input.get("hobby", ""))
        personality = normalize(user_input.get("personality", ""))
        career_goal = normalize(user_input.get("career_goal", ""))
        stream = normalize(user_input.get("stream", ""))
        course_type = normalize(user_input.get("course_type", "full-time"))

        try:
            affordability = float(user_input.get("affordability", 1e9))
        except:
            affordability = 1e9

        career_unknown = career_goal in ["i am not sure yet", "unknown", ""]

        # ---------------- FILTER ----------------
        if not career_unknown:
            filtered_df = data[
                (data["Career_Goal"].str.lower() == career_goal) &
                (data["Stream"].str.lower() == stream) &
                (data["Course_Type"].str.lower() == course_type) &
                (data["Average_Fees"] <= affordability)
            ]
        else:
            filtered_df = data[
                (data["Stream"].str.lower() == stream) &
                (data["Course_Type"].str.lower() == course_type) &
                (data["Average_Fees"] <= affordability)
            ]

        if filtered_df.empty and not career_unknown:
            filtered_df = data[
                (data["Career_Goal"].str.lower() == career_goal) &
                (data["Course_Type"].str.lower() == course_type) &
                (data["Average_Fees"] <= affordability)
            ]

        # ---------------- NO RECOMMENDATIONS ----------------
        if filtered_df.empty:
            return jsonify([{
                "course": "No recommendations available at the moment",
                "top_recommended_institutions": [],
                "course_type": "",
                "average_fees": 0,
                "match_score": 0,
                "note": "We couldn't find courses that match your current preferences. Try updating your interests, budget, or stream to see more options."
            }]), 200

        # ---------------- SCORING ----------------
        scored_rows = []
        for _, row in filtered_df.iterrows():
            score = 0
            if not career_unknown and normalize(row.get("Career_Goal", "")) == career_goal:
                score += 40
            if normalize(row.get("Stream", "")) == stream:
                score += 20
            if personality and normalize(row.get("Personality", "")) == personality:
                score += 25
            if hobby and normalize(row.get("Hobby", "")) == hobby:
                score += 15
            scored_rows.append((score, row))

        scored_rows = sorted(scored_rows, key=lambda x: x[0], reverse=True)

        # ---------------- BUILD RECOMMENDATIONS ----------------
        recommendations = []
        added_courses = set()
        for score, row in scored_rows:
            if len(recommendations) >= 3:
                break

            course_name = row.get("Recommended_Courses", "").strip()
            if not course_name or course_name in added_courses:
                continue

            colleges = [c.strip() for c in str(row.get("Nearby_Colleges", "")).split("|") if c.strip()]
            websites = [w.strip() for w in str(row.get("College_Websites", "")).split("|") if w.strip()]

            colleges_with_links = []
            for i, c in enumerate(colleges):
                w = websites[i] if i < len(websites) else None
                if w:
                    colleges_with_links.append(f"{c} ({w})")
                else:
                    colleges_with_links.append(c)

            recommendations.append({
                "course": course_name,
                "top_recommended_institutions": colleges_with_links[:3],  # up to 3 colleges
                "course_type": row.get("Course_Type"),
                "average_fees": float(row.get("Average_Fees", 0)),
                "match_score": score
            })
            added_courses.add(course_name)

        # ---------------- SAVE TO DATABASE ----------------
        if email:
            conn = get_db_connection()
            rec_json = json.dumps(recommendations)
            exists = conn.execute("SELECT 1 FROM recommendations WHERE email=?", (email,)).fetchone()
            if exists:
                conn.execute("UPDATE recommendations SET careers=? WHERE email=?", (rec_json, email))
            else:
                conn.execute("INSERT INTO recommendations (email, careers) VALUES (?,?)", (email, rec_json))
            conn.commit()
            conn.close()

        return jsonify(recommendations)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
# ---------------- DASHBOARDS ----------------
@app.route("/student/dashboard", methods=["GET"])
def student_dashboard():
    email = normalize(request.args.get("email",""))
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE email=?", (email,)).fetchone()
    if not student:
        conn.close()
        return jsonify({"error":"Student not found"}),404
    rec = conn.execute("SELECT * FROM recommendations WHERE email=?", (email,)).fetchone()
    careers = json.loads(rec["careers"]) if rec and rec["careers"] else []
    conn.close()
    return jsonify({"student": dict(student), "careers": careers})

@app.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    conn = get_db_connection()
    total_students = conn.execute("SELECT COUNT(*) AS total FROM students").fetchone()["total"]
    stream_stats = conn.execute("SELECT stream, COUNT(*) AS count FROM students GROUP BY stream").fetchall()
    stream_stats = [{"stream": s["stream"], "count": s["count"]} for s in stream_stats]
    conn.close()
    return jsonify({"total_students": total_students, "stream_stats": stream_stats})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
