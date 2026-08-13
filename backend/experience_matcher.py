import re
from title_data import TITLE_GROUPS, LEADERSHIP_WORDS, CERTIFICATION_KEYWORDS

YEARS_RE = re.compile(
    r"(\d{1,2})\+?\s*(?:to\s*\d{1,2}\s*)?(?:years?|yrs?)(?:\s+of)?(?:\s+(?:relevant|professional|industry|work))?\s*(?:experience)?",
    re.IGNORECASE,
)

MONTHS_RE = re.compile(r"(\d{1,2})\+?\s*months?", re.IGNORECASE)


def _extract_max_years(text: str) -> float:
    years = [int(m.group(1)) for m in YEARS_RE.finditer(text)]
    months = [int(m.group(1)) for m in MONTHS_RE.finditer(text)]
    max_years = max(years) if years else 0.0
    if months and max_years == 0:
        max_years = max(months) / 12.0
    return max_years


def _extract_titles(text: str) -> list:
    lower = text.lower()
    found = []
    for group in TITLE_GROUPS:
        for title in group:
            if title.lower() in lower:
                found.append(title)
    return sorted(set(found))


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


def _detect_certifications(text: str) -> list:
    lower = text.lower()
    certs = []
    for line in text.splitlines():
        line_lower = line.lower().strip()
        if any(kw in line_lower for kw in CERTIFICATION_KEYWORDS) and len(line_lower) > 5:
            certs.append(line.strip())
    return certs[:10]


def match_experience(resume_text: str, jd_text: str, jd_years_hint: float = 0.0) -> dict:
    resume_years = _extract_max_years(resume_text)
    jd_years_required = _extract_max_years(jd_text) or jd_years_hint

    resume_titles = _extract_titles(resume_text)
    jd_titles = _extract_titles(jd_text)

    leadership = any(w in resume_text.lower() for w in LEADERSHIP_WORDS)
    resume_certs = _detect_certifications(resume_text)
    jd_certs = _detect_certifications(jd_text)

    # Years (60 pts), title match (25 pts), certifications (15 pts)
    if jd_years_required == 0:
        years_score = 60.0
    elif resume_years >= jd_years_required:
        years_score = 60.0
    else:
        years_score = round(60.0 * (resume_years / jd_years_required), 1) if jd_years_required else 0.0

    title_score = 25.0 if _titles_equivalent(resume_titles, jd_titles) else 8.0

    cert_score = 15.0
    if jd_certs:
        cert_score = 15.0 if resume_certs else 5.0

    total = round(min(100.0, years_score + title_score + cert_score), 1)

    return {
        "resume_years": resume_years,
        "required_years": jd_years_required,
        "resume_titles": resume_titles,
        "jd_titles": jd_titles,
        "leadership_detected": leadership,
        "resume_certifications": resume_certs,
        "jd_certifications": jd_certs,
        "score": total,
    }
