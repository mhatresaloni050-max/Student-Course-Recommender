import sqlite3

DB_PATH = "student_reco.db"

def seed_data():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ------------------ COURSES ------------------
    courses = [
        ("BSc Computer Science", "Science", "Analytical", "coding,technology,gaming"),
        ("BCA", "Science", "Analytical", "coding,technology"),
        ("BCom", "Commerce", "Organized", "business,finance"),
        ("BA Psychology", "Arts", "Empathetic", "helping,reading"),
        ("BSc Animation", "Arts", "Creative", "drawing,design,gaming"),
        ("BBA", "Commerce", "Leadership", "business,management")
    ]

    cur.executemany("""
        INSERT INTO courses (name, stream, recommended_for_personality, related_hobbies)
        VALUES (?, ?, ?, ?)
    """, courses)

    # ------------------ COLLEGES ------------------
    colleges = [
        ("St Xavier's College", "Mumbai", 18.9380, 72.8354, "BSc Computer Science,BCom,BA Psychology"),
        ("NM College", "Mumbai", 19.1031, 72.8360, "BCom,BBA"),
        ("Mumbai University", "Mumbai", 19.0700, 72.8777, "BSc Computer Science,BSc Animation"),
        ("RA Podar College", "Mumbai", 19.0200, 72.8430, "BCom,BBA")
    ]

    cur.executemany("""
        INSERT INTO colleges (name, city, latitude, longitude, courses_offered)
        VALUES (?, ?, ?, ?, ?)
    """, colleges)

    conn.commit()
    conn.close()

    print("✅ Seed data inserted successfully")

if __name__ == "__main__":
    seed_data()
