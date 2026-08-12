"""
Job description parsing: extracts required/preferred skills, responsibilities,
experience requirement, education requirement, and certifications.
"""
import re
from dataclasses import dataclass, field
from typing import List

from app.data.skills_taxonomy import ALL_KNOWN_SKILLS, normalize_term, DEGREE_LEVELS

YEARS_REQ_RE = re.compile(
    r"(\d+)\+?\s*(?:-\s*\d+\s*)?(?:years?|yrs?)\s*(?:of)?\s*(?:relevant\s*)?experience",
    re.IGNORECASE,
)

PREFERRED_MARKERS = ["preferred", "nice to have", "bonus", "plus if", "a plus"]
REQUIRED_MARKERS = ["required", "must have", "requirements", "qualifications"]


@dataclass
class ParsedJD:
    raw_text: str
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)
    responsibilities: List[str] = field(default_factory=list)
    required_years_experience: float = 0.0
    required_education_level: int = 0
    required_titles: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)


def _extract_all_skills(text: str) -> set:
    lower = text.lower()
    found = set()
    for skill in ALL_KNOWN_SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, lower):
            found.add(normalize_term(skill))
    return found


def _split_preferred_vs_required(text: str, all_skills: set) -> tuple:
    """Roughly bucket skills into required vs preferred based on nearby section markers."""
    lower = text.lower()
    preferred_idx = min([lower.find(m) for m in PREFERRED_MARKERS if lower.find(m) != -1], default=-1)

    if preferred_idx == -1:
        return sorted(all_skills), []

    preferred_section = text[preferred_idx:]
    preferred_skills = _extract_all_skills(preferred_section)
    required_skills = all_skills - preferred_skills
    return sorted(required_skills), sorted(preferred_skills)


def _extract_years(text: str) -> float:
    matches = YEARS_REQ_RE.findall(text)
    years = [float(m) for m in matches if m]
    return max(years) if years else 0.0


def _extract_education_level(text: str) -> int:
    lower = text.lower()
    levels = []
    for degree, level in DEGREE_LEVELS.items():
        pattern = r"(?<![a-zA-Z])" + re.escape(degree) + r"(?![a-zA-Z])"
        if re.search(pattern, lower):
            levels.append(level)
    return max(levels) if levels else 0


def _extract_responsibilities(text: str) -> List[str]:
    lines = [l.strip("-• \t") for l in text.split("\n") if l.strip()]
    bullets = [l for l in lines if len(l) > 15 and len(l) < 250]
    return bullets[:15]


def _extract_titles(text: str) -> List[str]:
    from app.data.skills_taxonomy import TITLE_EQUIVALENCE_GROUPS
    lower = text.lower()
    found = []
    for group in TITLE_EQUIVALENCE_GROUPS:
        for title in group:
            if title in lower:
                found.append(title)
    return sorted(set(found))


def parse_jd(text: str) -> ParsedJD:
    all_skills = _extract_all_skills(text)
    required, preferred = _split_preferred_vs_required(text, all_skills)

    cert_keywords = ["certified", "certification", "certificate"]
    cert_lines = [l.strip("-• \t") for l in text.split("\n")
                  if any(k in l.lower() for k in cert_keywords) and len(l.strip()) > 3]

    return ParsedJD(
        raw_text=text,
        required_skills=required,
        preferred_skills=preferred,
        responsibilities=_extract_responsibilities(text),
        required_years_experience=_extract_years(text),
        required_education_level=_extract_education_level(text),
        required_titles=_extract_titles(text),
        certifications=cert_lines[:10],
    )
