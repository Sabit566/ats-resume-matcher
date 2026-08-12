import re
from skills_data import ALL_SURFACE_FORMS, SURFACE_TO_CANONICAL, canonical_category


def extract_skills(text: str) -> set:
    """Find every known skill surface form present in text, return canonical names."""
    if not text:
        return set()
    lowered = text.lower()
    found = set()
    for form in ALL_SURFACE_FORMS:
        # word-boundary match, careful with forms containing punctuation like C#, .NET, CI/CD
        pattern = r"(?<![a-z0-9])" + re.escape(form) + r"(?![a-z0-9])"
        if re.search(pattern, lowered):
            found.add(SURFACE_TO_CANONICAL[form])
    return found


def match_skills(resume_text: str, jd_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    score = 100.0 if not jd_skills else round(len(matched) / len(jd_skills) * 100, 1)

    missing_by_category = {}
    for skill in missing:
        cat = canonical_category(skill)
        missing_by_category.setdefault(cat, []).append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_resume_skills": extra,
        "missing_skills_by_category": missing_by_category,
        "score": score,
    }
