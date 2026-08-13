import re
from skills_data import ALL_SURFACE_FORMS, SURFACE_TO_CANONICAL
from title_data import TITLE_GROUPS, CERTIFICATION_KEYWORDS

REQUIRED_MARKERS = [
    "requirements", "required qualifications", "must have", "minimum qualifications",
    "required skills", "qualifications", "what you need", "what we're looking for",
    "you have", "you bring",
]
PREFERRED_MARKERS = [
    "preferred qualifications", "nice to have", "preferred skills", "bonus",
    "plus if", "a plus", "desired", "would be great", "ideally",
]
RESPONSIBILITY_MARKERS = [
    "responsibilities", "duties", "what you'll do", "key responsibilities",
    "role overview", "about the role", "job description",
]

YEARS_RE = re.compile(
    r"(\d{1,2})\+?\s*(?:to\s*\d{1,2}\s*)?(?:years?|yrs?)(?:\s+of)?(?:\s+(?:relevant|professional|industry|work))?\s*(?:experience)?",
    re.IGNORECASE,
)

DEGREE_LEVELS = {
    "phd": 4, "ph.d": 4, "doctorate": 4, "doctoral": 4,
    "master": 3, "masters": 3, "mba": 3, "m.s": 3, "msc": 3,
    "bachelor": 2, "bachelors": 2, "b.s": 2, "bsc": 2, "b.tech": 2,
    "associate": 1, "diploma": 1, "vocational": 1,
}


def _find_block(text: str, markers: list, block_size: int = 800) -> str:
    lower = text.lower()
    for marker in markers:
        idx = lower.find(marker)
        if idx != -1:
            return text[idx: idx + block_size]
    return ""


def _extract_skills(text: str) -> set:
    if not text:
        return set()
    lowered = text.lower()
    found = set()
    for form in ALL_SURFACE_FORMS:
        pattern = r"(?<![a-z0-9])" + re.escape(form) + r"(?![a-z0-9])"
        if re.search(pattern, lowered):
            found.add(SURFACE_TO_CANONICAL[form])
    return found


def _extract_years(text: str) -> float:
    matches = [int(m.group(1)) for m in YEARS_RE.finditer(text)]
    return float(max(matches)) if matches else 0.0


def _extract_education_level(text: str) -> int:
    lower = text.lower()
    level = 0
    for keyword, lvl in DEGREE_LEVELS.items():
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(keyword) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, lower):
            level = max(level, lvl)
    return level


def _extract_titles(text: str) -> list:
    lower = text.lower()
    found = []
    for group in TITLE_GROUPS:
        for title in group:
            if title.lower() in lower:
                found.append(title)
    return sorted(set(found))


def _extract_certifications(text: str) -> list:
    certs = []
    for line in text.splitlines():
        line_lower = line.lower().strip()
        if any(kw in line_lower for kw in CERTIFICATION_KEYWORDS) and len(line_lower) > 5:
            certs.append(line.strip())
    return certs[:10]


def _extract_responsibilities(text: str) -> list:
    block = _find_block(text, RESPONSIBILITY_MARKERS, 1200) or text
    lines = [l.strip("-• \t") for l in block.splitlines() if l.strip()]
    bullets = [l for l in lines if 15 < len(l) < 300]
    return bullets[:15]


def parse_job_description(text: str) -> dict:
    required_block = _find_block(text, REQUIRED_MARKERS) or text
    preferred_block = _find_block(text, PREFERRED_MARKERS)
    all_skills = _extract_skills(text)
    required_skills = _extract_skills(required_block)
    preferred_skills = _extract_skills(preferred_block) - required_skills if preferred_block else set()

    if not required_skills:
        required_skills = all_skills - preferred_skills

    return {
        "raw_text": text,
        "required_block": required_block,
        "preferred_block": preferred_block,
        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),
        "responsibilities": _extract_responsibilities(text),
        "required_years": _extract_years(text),
        "required_education_level": _extract_education_level(text),
        "jd_titles": _extract_titles(text),
        "certifications": _extract_certifications(text),
    }
