def build_strengths(skill_result: dict, experience_result: dict) -> list:
    strengths = list(skill_result["matched_skills"])
    if experience_result.get("leadership_detected"):
        strengths.append("Leadership")
    return strengths


def build_suggestions(skill_result: dict, experience_result: dict,
                       education_result: dict, keyword_result: dict) -> list:
    suggestions = []

    missing_by_cat = skill_result.get("missing_skills_by_category", {})
    for cat, skills in missing_by_cat.items():
        if skills:
            example = skills[0]
            suggestions.append(f"Add {cat.lower()} experience with {example}, or mention it directly if you already have it.")

    if experience_result["required_years"] and experience_result["resume_years"] < experience_result["required_years"]:
        gap = experience_result["required_years"] - experience_result["resume_years"]
        suggestions.append(f"Highlight roughly {gap} more year(s) of relevant experience, or reframe existing projects to show that depth.")

    if not experience_result.get("leadership_detected"):
        suggestions.append("Include leadership or mentorship examples (e.g. 'led', 'mentored', 'managed a team of...').")

    if education_result["score"] < 100:
        suggestions.append(f"Job prefers {education_result['required_degree']}; consider noting relevant certifications or coursework if applicable.")

    missing_keywords = [kw for kw in keyword_result.get("top_keywords", [])
                         if kw not in keyword_result.get("covered_keywords", [])]
    if missing_keywords:
        sample = ", ".join(missing_keywords[:5])
        suggestions.append(f"Weave in key JD terms where genuinely true: {sample}.")

    suggestions.append("Quantify achievements using measurable metrics (%, $, time saved, users impacted).")

    return suggestions


def build_report(semantic_result, skill_result, experience_result,
                  education_result, keyword_result, score_result, resume_meta) -> dict:
    return {
        "candidate": {
            "name": resume_meta.get("name", ""),
            "email": resume_meta.get("email", ""),
            "phone": resume_meta.get("phone", ""),
        },
        "overall_score": score_result["overall_score"],
        "match_level": score_result["match_level"],
        "breakdown": {
            "semantic_similarity": semantic_result["score"],
            "skills_match": skill_result["score"],
            "experience_match": experience_result["score"],
            "education_match": education_result["score"],
            "keyword_coverage": keyword_result["score"],
        },
        "weights": score_result["weights"],
        "semantic_method": semantic_result["method"],
        "skills": {
            "matched": skill_result["matched_skills"],
            "missing": skill_result["missing_skills"],
            "missing_by_category": skill_result["missing_skills_by_category"],
            "extra": skill_result["extra_resume_skills"],
        },
        "experience": experience_result,
        "education": education_result,
        "keyword": keyword_result,
        "strengths": build_strengths(skill_result, experience_result),
        "suggestions": build_suggestions(skill_result, experience_result, education_result, keyword_result),
    }
