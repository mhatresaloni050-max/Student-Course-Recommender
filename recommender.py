import pandas as pd

def recommend_career(stream, personality, interests):
    df = pd.read_csv("careers.csv")


    df = df[df["stream"].str.lower() == stream.lower()]


    df = df[df["required_personality"].str.lower() == personality.lower()]


    def interest_score(courses):
        score = 0
        for interest in interests:
            if interest.lower() in courses.lower():
                score += 1
        return score

    df["score"] = df["suggested_courses"].apply(interest_score)


    df = df.sort_values(by="score", ascending=False)


    top = df.iloc[0]

    return {
        "career": top["career"],
        "suggested_courses": top["suggested_courses"].split(";")
    }
