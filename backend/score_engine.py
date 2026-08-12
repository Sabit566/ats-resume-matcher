WEIGHTS = {
    "semantic": 0.40,
    "skills": 0.25,
    "experience": 0.15,
    "education": 0.10,
    "keyword": 0.10,
}


def compute_overall_score(semantic_score, skills_score, experience_score,
                           education_score, keyword_score) -> dict:
    overall = (
        semantic_score * WEIGHTS["semantic"]
        + skills_score * WEIGHTS["skills"]
        + experience_score * WEIGHTS["experience"]
        + education_score * WEIGHTS["education"]
        + keyword_score * WEIGHTS["keyword"]
    )
    overall = round(min(100.0, max(0.0, overall)), 1)

    if overall >= 85:
        level = "Excellent"
    elif overall >= 70:
        level = "Good"
    elif overall >= 50:
        level = "Moderate"
    else:
        level = "Low"

    return {
        "overall_score": overall,
        "match_level": level,
        "weights": WEIGHTS,
    }
