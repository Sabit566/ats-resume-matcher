import re

DEGREE_LEVELS = {
    # Doctorate
    "phd": 4, "ph.d": 4, "ph.d.": 4, "doctorate": 4, "doctoral": 4,
    "doctor of philosophy": 4, "doctor of medicine": 4, "md": 4, "d.o.": 4,
    "juris doctor": 4, "jd": 4, "doctor of nursing practice": 4, "dnp": 4,
    # Master
    "master": 3, "masters": 3, "master's": 3, "m.s": 3, "m.s.": 3,
    "msc": 3, "m.sc": 3, "mba": 3, "m.eng": 3, "m.a.": 3, "ma": 3,
    "master of science": 3, "master of arts": 3, "master of business administration": 3,
    # Bachelor
    "bachelor": 2, "bachelors": 2, "bachelor's": 2, "b.s": 2, "b.s.": 2,
    "bsc": 2, "b.sc": 2, "b.eng": 2, "b.tech": 2, "btech": 2, "be": 2,
    "b.e.": 2, "undergraduate": 2, "b.a.": 2, "ba": 2,
    "bachelor of science": 2, "bachelor of arts": 2, "bachelor of engineering": 2,
    # Associate / Diploma
    "associate": 1, "associate's": 1, "a.s.": 1, "a.a.": 1, "aas": 1,
    "diploma": 1, "vocational": 1, "certificate program": 1, "trade school": 1,
    "high school": 0, "ged": 0, "secondary school": 0,
}

DEGREE_LABELS = {
    0: "High School / Not detected",
    1: "Associate / Diploma",
    2: "Bachelor's",
    3: "Master's",
    4: "Doctorate / Professional",
}

CERT_PATTERNS = [
    r"\b(?:certified|certification|certificate|licensed|license)\b",
    r"\b(?:cpa|cfa|cma|pmp|csm|aws certified|google certified|microsoft certified)\b",
    r"\b(?:rn|lpn|cna|bls|acls|osha|six sigma|lean six sigma)\b",
    r"\b(?:bar admission|paralegal certification|comptia|cissp|ceh)\b",
]


def _max_degree_level(text: str) -> int:
    lower = text.lower()
    level = 0
    for keyword, lvl in DEGREE_LEVELS.items():
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(keyword) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, lower):
            level = max(level, lvl)
    return level


def _extract_certifications(text: str) -> list:
    found = []
    lower = text.lower()
    for line in text.splitlines():
        line_lower = line.lower().strip()
        if any(re.search(p, line_lower) for p in CERT_PATTERNS) and len(line_lower) > 4:
            found.append(line.strip())
    return found[:10]


def match_education(
    resume_text: str,
    jd_text: str,
    jd_level_hint: int = 0,
    resume_sections: dict = None,
) -> dict:
    edu_text = resume_text
    if resume_sections:
        edu_parts = [
            resume_sections.get("education", ""),
            resume_sections.get("certifications", ""),
        ]
        combined = "\n".join(p for p in edu_parts if p)
        if combined.strip():
            edu_text = combined + "\n" + resume_text

    resume_level = _max_degree_level(edu_text)
    jd_level = _max_degree_level(jd_text) or jd_level_hint

    resume_certs = _extract_certifications(edu_text)
    jd_certs = _extract_certifications(jd_text)

    # Degree score (75 pts) + certification bonus (25 pts)
    if jd_level == 0:
        degree_score = 75.0
    elif resume_level >= jd_level:
        degree_score = 75.0
    elif resume_level == jd_level - 1:
        degree_score = 45.0
    else:
        degree_score = 20.0 if resume_level > 0 else 0.0

    cert_score = 25.0
    if jd_certs:
        cert_score = 25.0 if resume_certs else 8.0

    score = round(min(100.0, degree_score + cert_score), 1)

    return {
        "resume_degree": DEGREE_LABELS.get(resume_level, "Not detected"),
        "required_degree": DEGREE_LABELS.get(jd_level, "Not specified"),
        "resume_certifications": resume_certs,
        "required_certifications": jd_certs,
        "score": score,
    }
