import re

DEGREE_LEVELS = {
    "phd": 3, "ph.d": 3, "doctorate": 3, "doctoral": 3,
    "master": 2, "m.s": 2, "msc": 2, "mba": 2, "m.eng": 2,
    "bachelor": 1, "b.s": 1, "bsc": 1, "b.eng": 1, "b.tech": 1, "undergraduate": 1,
}

DEGREE_LABELS = {1: "Bachelor's", 2: "Master's", 3: "PhD"}


def _max_degree_level(text: str) -> int:
    lower = text.lower()
    level = 0
    for keyword, lvl in DEGREE_LEVELS.items():
        if keyword in lower:
            level = max(level, lvl)
    return level


def match_education(resume_text: str, jd_text: str) -> dict:
    resume_level = _max_degree_level(resume_text)
    jd_level = _max_degree_level(jd_text)

    if jd_level == 0:
        score = 100.0
    elif resume_level >= jd_level:
        score = 100.0
    elif resume_level == jd_level - 1:
        score = 60.0
    else:
        score = 30.0 if resume_level > 0 else 0.0

    return {
        "resume_degree": DEGREE_LABELS.get(resume_level, "Not detected"),
        "required_degree": DEGREE_LABELS.get(jd_level, "Not specified"),
        "score": score,
    }
