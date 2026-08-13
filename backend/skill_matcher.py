import re
from skills_data import ALL_SURFACE_FORMS, SURFACE_TO_CANONICAL, canonical_category


def extract_skills(text: str) -> set:
    """Find every known skill surface form present in text, return canonical names."""
    if not text:
        return set()
    lowered = text.lower()
    found = set()
    for form in ALL_SURFACE_FORMS:
        pattern = r"(?<![a-z0-9])" + re.escape(form) + r"(?![a-z0-9])"
        if re.search(pattern, lowered):
            found.add(SURFACE_TO_CANONICAL[form])
    return found


def _score_skill_sets(resume_skills: set, required: set, preferred: set) -> float:
    """Required skills weigh 70%, preferred skills weigh 30%."""
    if not required and not preferred:
        return 100.0

    req_score = 100.0
    if required:
        req_matched = len(resume_skills & required)
        req_score = req_matched / len(required) * 100

    pref_score = 100.0
    if preferred:
        pref_matched = len(resume_skills & preferred)
        pref_score = pref_matched / len(preferred) * 100

    if required and preferred:
        return round(req_score * 0.7 + pref_score * 0.3, 1)
    if required:
        return round(req_score, 1)
    return round(pref_score, 1)


def match_skills(
    resume_text: str,
    jd_text: str,
    required_block: str = "",
    preferred_block: str = "",
) -> dict:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    req_text = required_block or jd_text
    pref_text = preferred_block or ""
    required_skills = extract_skills(req_text)
    preferred_skills = extract_skills(pref_text) - required_skills if pref_text else set()

    if not required_skills and not preferred_skills:
        required_skills = jd_skills

    matched = sorted(resume_skills & jd_skills)
    missing_required = sorted(required_skills - resume_skills)
    missing_preferred = sorted(preferred_skills - resume_skills)
    missing = sorted(set(missing_required) | set(missing_preferred))
    extra = sorted(resume_skills - jd_skills)

    score = _score_skill_sets(resume_skills, required_skills, preferred_skills)

    missing_by_category = {}
    for skill in missing:
        cat = canonical_category(skill)
        missing_by_category.setdefault(cat, []).append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "extra_resume_skills": extra,
        "missing_skills_by_category": missing_by_category,
        "required_skills_count": len(required_skills),
        "preferred_skills_count": len(preferred_skills),
        "score": score,
    }
