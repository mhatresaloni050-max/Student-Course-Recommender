import pandas as pd

def recommend_career(stream, personality, interests):
    df = pd.read_csv("careers.csv")

    # 1. Filter by stream
    df = df[df["stream"].str.lower() == stream.lower()]

    # 2. Filter by personality
    df = df[df["required_personality"].str.lower() == personality.lower()]

    # 3. Interest matching score
    def interest_score(courses):
        score = 0
        for interest in interests:
            if interest.lower() in courses.lower():
                score += 1
        return score

    df["score"] = df["suggested_courses"].apply(interest_score)

    # 4. Sort by best match
    df = df.sort_values(by="score", ascending=False)

    # 5. Pick best
    top = df.iloc[0]

    return {
        "career": top["career"],
        "suggested_courses": top["suggested_courses"].split(";")
    }
