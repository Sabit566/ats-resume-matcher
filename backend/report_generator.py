CATEGORY_SUGGESTIONS = {
    "Technology": "Highlight specific technologies, projects, and measurable engineering outcomes.",
    "Healthcare": "Emphasize clinical experience, patient outcomes, licenses, and compliance training.",
    "Finance": "Show quantifiable financial impact, certifications (CPA/CFA), and regulatory knowledge.",
    "Sales & Marketing": "Include quota attainment, pipeline growth, campaign ROI, and CRM proficiency.",
    "Design & Creative": "Link to your portfolio and describe design process, tools, and user impact.",
    "Operations & HR": "Stress process improvements, team size managed, and operational KPIs achieved.",
    "Legal": "Note bar status, practice areas, case types, and compliance/regulatory experience.",
    "Education & Research": "List publications, grants, teaching experience, and research methodologies.",
    "Trades & Engineering": "Mention licenses, safety certifications, equipment, and project scale.",
    "General": "Tailor your resume keywords to mirror the job description language.",
}


def build_strengths(skill_result: dict, experience_result: dict, education_result: dict) -> list:
    strengths = list(skill_result["matched_skills"][:8])
    if experience_result.get("leadership_detected"):
        strengths.append("Leadership experience")
    if experience_result.get("resume_certifications"):
        strengths.append("Relevant certifications")
    if education_result.get("resume_certifications"):
        strengths.append("Professional credentials")
    return strengths


def build_suggestions(
    skill_result: dict,
    experience_result: dict,
    education_result: dict,
    keyword_result: dict,
    job_category: str = "General",
) -> list:
    suggestions = []

    missing_required = skill_result.get("missing_required_skills", [])
    if missing_required:
        sample = ", ".join(missing_required[:4])
        suggestions.append(f"Add required skills explicitly if you have them: {sample}.")

    missing_by_cat = skill_result.get("missing_skills_by_category", {})
    for cat, skills in missing_by_cat.items():
        if skills and cat != "Other":
            example = skills[0]
            suggestions.append(
                f"Strengthen your {cat.lower()} profile — consider adding {example} if applicable."
            )

    if experience_result["required_years"] and experience_result["resume_years"] < experience_result["required_years"]:
        gap = experience_result["required_years"] - experience_result["resume_years"]
        suggestions.append(
            f"Highlight roughly {gap:.0f} more year(s) of relevant experience, "
            "or reframe projects to show equivalent depth."
        )

    if not experience_result.get("leadership_detected"):
        suggestions.append(
            "Include leadership or mentorship examples (e.g. 'led', 'mentored', 'managed a team of...')."
        )

    if education_result["score"] < 100:
        req = education_result["required_degree"]
        if req != "Not specified":
            suggestions.append(
                f"Job prefers {req}; note relevant degrees, certifications, or coursework."
            )

    missing_keywords = keyword_result.get("missing_keywords", [])
    if missing_keywords:
        sample = ", ".join(missing_keywords[:5])
        suggestions.append(f"Weave in key JD terms where genuinely true: {sample}.")

    suggestions.append(CATEGORY_SUGGESTIONS.get(job_category, CATEGORY_SUGGESTIONS["General"]))
    suggestions.append("Quantify achievements using measurable metrics (%, $, time saved, users impacted).")

    return suggestions


def build_report(
    semantic_result,
    skill_result,
    experience_result,
    education_result,
    keyword_result,
    score_result,
    resume_meta,
    job_category: str = "General",
    category_scores: dict = None,
    jd_meta: dict = None,
) -> dict:
    jd_meta = jd_meta or {}
    return {
        "candidate": {
            "name": resume_meta.get("name", ""),
            "email": resume_meta.get("email", ""),
            "phone": resume_meta.get("phone", ""),
        },
        "job_category": job_category,
        "category_scores": category_scores or {},
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
            "missing_required": skill_result.get("missing_required_skills", []),
            "missing_preferred": skill_result.get("missing_preferred_skills", []),
            "missing_by_category": skill_result["missing_skills_by_category"],
            "extra": skill_result["extra_resume_skills"],
        },
        "experience": experience_result,
        "education": education_result,
        "keyword": keyword_result,
        "job_description": {
            "responsibilities": jd_meta.get("responsibilities", []),
            "required_skills": jd_meta.get("required_skills", []),
            "preferred_skills": jd_meta.get("preferred_skills", []),
            "certifications": jd_meta.get("certifications", []),
        },
        "strengths": build_strengths(skill_result, experience_result, education_result),
        "suggestions": build_suggestions(
            skill_result, experience_result, education_result, keyword_result, job_category
        ),
    }
