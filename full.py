import pandas as pd
import itertools

# Personality types
personalities = ["analytical", "creative", "logical", "leadership"]

# All hobbies from your frontend
hobbies = [
    "Coding", "Robotics", "Electronics", "AI & Machine Learning", "Data Science",
    "Lab Work / Research", "Healthcare", "Medicine", "Nursing",
    "Painting", "Drawing", "Photography", "Fashion Design",
    "Animation", "Film Making", "Music", "Dance", "Writing", "Storytelling",
    "Football", "Basketball", "Yoga", "Wellness", "Martial Arts", "Athletics", "Adventure Sports",
    "Volunteering", "Gaming", "Puzzle Solving"
]

# Streams
streams = ["Science", "Commerce", "Arts"]

# Course types
course_types = ["full-time", "part-time"]

# Map career goals to recommended course and 2 Indian colleges + websites
career_map = {
    "Software Developer": (
        "B.Tech Computer Science",
        "IIT Delhi|Indian Institute of Technology Delhi - https://home.iitd.ac.in/|IIT Bombay|Indian Institute of Technology Bombay - https://www.iitb.ac.in/",
        200000
    ),
    "Data Scientist": (
        "B.Sc Data Science",
        "IIT Madras|Indian Institute of Technology Madras - https://www.iitm.ac.in/|IIIT Hyderabad|International Institute of Information Technology Hyderabad - https://www.iiit.ac.in/",
        220000
    ),
    "Cybersecurity Expert": (
        "B.Tech Cybersecurity",
        "IIIT Hyderabad|International Institute of Information Technology Hyderabad - https://www.iiit.ac.in/|NIT Warangal|National Institute of Technology Warangal - https://www.nitw.ac.in/",
        190000
    ),
    "AI Engineer": (
        "B.Tech AI & Machine Learning",
        "IIT Kharagpur|Indian Institute of Technology Kharagpur - https://www.iitkgp.ac.in/|VIT Vellore|Vellore Institute of Technology - https://vit.ac.in/",
        210000
    ),
    "Game Developer": (
        "B.Sc Game Development",
        "MIT ADT University|MIT Art, Design & Technology University - https://mituniversity.ac.in/|JK Lakshmipat University|JKLU Jaipur - https://www.jklu.edu.in/",
        180000
    ),
    "Cloud Engineer": (
        "B.Tech Cloud Computing",
        "Manipal University|Manipal Academy of Higher Education - https://manipal.edu/|SRM University|SRM Institute of Science and Technology - https://www.srmist.edu.in/",
        200000
    ),
    "Mechanical Engineer": (
        "B.Tech Mechanical Engineering",
        "IIT Kanpur|Indian Institute of Technology Kanpur - https://www.iitk.ac.in/|NIT Trichy|National Institute of Technology Tiruchirappalli - https://www.nitt.edu/",
        220000
    ),
    "Civil Engineer": (
        "B.Tech Civil Engineering",
        "IIT Roorkee|Indian Institute of Technology Roorkee - https://www.iitr.ac.in/|Anna University|Anna University - https://www.annauniv.edu/",
        200000
    ),
    "Electrical Engineer": (
        "B.Tech Electrical Engineering",
        "IIT Bombay|Indian Institute of Technology Bombay - https://www.iitb.ac.in/|NIT Calicut|National Institute of Technology Calicut - https://www.nitc.ac.in/",
        210000
    ),
    "Doctor": (
        "MBBS",
        "AIIMS Delhi|All India Institute of Medical Sciences Delhi - https://www.aiims.edu/|CMC Vellore|Christian Medical College Vellore - https://www.cmch-vellore.edu/",
        500000
    ),
    # Add more mappings for each career from your dropdown as needed
}

# Generate CSV rows
rows = []
for personality, hobby, stream, course_type in itertools.product(personalities, hobbies, streams, course_types):
    for career_goal, (course, colleges, fees) in career_map.items():
        rows.append({
            "Personality": personality.lower(),
            "Hobby": hobby.lower(),
            "Stream": stream.lower(),
            "Career_Goal": career_goal.lower(),
            "Recommended_Courses": course,
            "Nearby_Colleges": colleges,
            "Course_Type": course_type.lower(),
            "Average_Fees": fees
        })

df = pd.DataFrame(rows)
df.to_csv("full_recommendation_data.csv", index=False)
print("✅ CSV generated: full_recommendation_data.csv")
