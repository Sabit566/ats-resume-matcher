from job_categories import weights_for_category, DEFAULT_WEIGHTS


def compute_overall_score(
    semantic_score,
    skills_score,
    experience_score,
    education_score,
    keyword_score,
    job_category: str = "General",
) -> dict:
    weights = weights_for_category(job_category)

    overall = (
        semantic_score * weights["semantic"]
        + skills_score * weights["skills"]
        + experience_score * weights["experience"]
        + education_score * weights["education"]
        + keyword_score * weights["keyword"]
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
        "weights": weights,
        "job_category": job_category,
    }
