import re

YEARS_RE = re.compile(r"(\d{1,2})\+?\s*(?:to\s*\d{1,2}\s*)?years?", re.IGNORECASE)

TITLE_GROUPS = [
    ["Principal Software Engineer", "Lead Software Engineer", "Senior Software Engineer",
     "Engineering Lead", "Staff Software Engineer"],
    ["Software Engineer", "Software Developer", "Backend Engineer", "Frontend Engineer",
     "Full Stack Engineer", "Full Stack Developer"],
    ["Data Scientist", "Machine Learning Engineer", "ML Engineer", "AI Engineer"],
    ["Engineering Manager", "Technical Lead", "Tech Lead", "Team Lead"],
    ["DevOps Engineer", "Site Reliability Engineer", "SRE", "Cloud Engineer"],
]

LEADERSHIP_WORDS = ["led", "managed", "mentored", "supervised", "directed", "spearheaded"]


def _extract_max_years(text: str) -> int:
    years = [int(m.group(1)) for m in YEARS_RE.finditer(text)]
    return max(years) if years else 0


def _extract_titles(text: str) -> list:
    lower = text.lower()
    found = []
    for group in TITLE_GROUPS:
        for title in group:
            if title.lower() in lower:
                found.append(title)
    return found


def _titles_equivalent(resume_titles: list, jd_titles: list) -> bool:
    if not jd_titles:
        return True
    for group in TITLE_GROUPS:
        group_lower = [t.lower() for t in group]
        jd_hit = any(t.lower() in group_lower for t in jd_titles)
        resume_hit = any(t.lower() in group_lower for t in resume_titles)
        if jd_hit and resume_hit:
            return True
    return False


def match_experience(resume_text: str, jd_text: str) -> dict:
    resume_years = _extract_max_years(resume_text)
    jd_years_required = _extract_max_years(jd_text)

    resume_titles = _extract_titles(resume_text)
    jd_titles = _extract_titles(jd_text)

    leadership = any(w in resume_text.lower() for w in LEADERSHIP_WORDS)

    # Years component (up to 70 of the 100 points), title component (30 points)
    if jd_years_required == 0:
        years_score = 70.0
    elif resume_years >= jd_years_required:
        years_score = 70.0
    else:
        years_score = round(70.0 * (resume_years / jd_years_required), 1) if jd_years_required else 0.0

    title_score = 30.0 if _titles_equivalent(resume_titles, jd_titles) else 10.0
    total = round(min(100.0, years_score + title_score), 1)

    return {
        "resume_years": resume_years,
        "required_years": jd_years_required,
        "resume_titles": resume_titles,
        "jd_titles": jd_titles,
        "leadership_detected": leadership,
        "score": total,
    }
