"""
Resume parsing: extracts raw text from PDF/DOCX/TXT and pulls out
structured fields (name, email, phone, skills, experience, education,
projects, certifications, achievements).
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional

from app.data.skills_taxonomy import ALL_KNOWN_SKILLS, normalize_term

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}")
YEARS_EXP_RE = re.compile(
    r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)?",
    re.IGNORECASE,
)
SECTION_HEADERS = {
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "education": ["education", "academic background"],
    "projects": ["projects", "personal projects", "academic projects"],
    "certifications": ["certifications", "certificates", "licenses"],
    "achievements": ["achievements", "awards", "honors"],
    "skills": ["skills", "technical skills", "core competencies"],
}


@dataclass
class ParsedResume:
    raw_text: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    years_experience: float = 0.0
    job_titles: List[str] = field(default_factory=list)
    is_leadership: bool = False
    companies: List[str] = field(default_factory=list)
    education_entries: List[dict] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    sections: dict = field(default_factory=dict)


def extract_text_from_file(path: str) -> str:
    """Extract raw text from a PDF, DOCX, or TXT file on disk."""
    lower = path.lower()
    if lower.endswith(".pdf"):
        return _extract_pdf(path)
    if lower.endswith(".docx"):
        return _extract_docx(path)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _extract_pdf(path: str) -> str:
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    except ImportError:
        import fitz  # PyMuPDF fallback
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)


def _extract_docx(path: str) -> str:
    import docx
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs)


def _split_sections(text: str) -> dict:
    """Naive section splitter based on common resume headers."""
    lines = text.split("\n")
    sections = {}
    current = "header"
    buffer = []
    for line in lines:
        stripped = line.strip().lower().rstrip(":")
        matched_section = None
        for key, headers in SECTION_HEADERS.items():
            if stripped in headers or (len(stripped) < 40 and any(stripped == h for h in headers)):
                matched_section = key
                break
        if matched_section:
            if buffer:
                sections.setdefault(current, []).extend(buffer)
            current = matched_section
            buffer = []
        else:
            buffer.append(line)
    if buffer:
        sections.setdefault(current, []).extend(buffer)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def _extract_skills(text: str) -> List[str]:
    lower = text.lower()
    found = set()
    for skill in ALL_KNOWN_SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, lower):
            found.add(normalize_term(skill))
    return sorted(found)


def _extract_years_experience(text: str) -> float:
    matches = YEARS_EXP_RE.findall(text)
    years = [float(m) for m in matches if m]
    return max(years) if years else 0.0


def _extract_job_titles(text: str) -> List[str]:
    from app.data.skills_taxonomy import TITLE_EQUIVALENCE_GROUPS
    lower = text.lower()
    found = []
    for group in TITLE_EQUIVALENCE_GROUPS:
        for title in group:
            if title in lower:
                found.append(title)
    return sorted(set(found))


def _extract_education(text: str) -> List[dict]:
    from app.data.skills_taxonomy import DEGREE_LEVELS
    lower = text.lower()
    entries = []
    for degree, level in DEGREE_LEVELS.items():
        pattern = r"(?<![a-zA-Z])" + re.escape(degree) + r"(?![a-zA-Z])"
        if re.search(pattern, lower):
            entries.append({"degree": degree, "level": level})
    # Dedup by level, keep highest representation
    seen_levels = {}
    for e in entries:
        seen_levels[e["level"]] = e["degree"]
    return [{"degree": v, "level": k} for k, v in sorted(seen_levels.items(), reverse=True)]


def parse_resume(text: str) -> ParsedResume:
    sections = _split_sections(text)
    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)

    leadership_keywords = ["led ", "lead ", "managed ", "mentored", "supervised", "directed team"]
    is_leadership = any(k in text.lower() for k in leadership_keywords)

    resume = ParsedResume(
        raw_text=text,
        email=email_match.group(0) if email_match else None,
        phone=phone_match.group(0).strip() if phone_match else None,
        skills=_extract_skills(text),
        years_experience=_extract_years_experience(text),
        job_titles=_extract_job_titles(text),
        is_leadership=is_leadership,
        education_entries=_extract_education(text),
        sections=sections,
    )

    if "projects" in sections:
        resume.projects = [l.strip("-• \t") for l in sections["projects"].split("\n") if l.strip()][:20]
    if "certifications" in sections:
        resume.certifications = [l.strip("-• \t") for l in sections["certifications"].split("\n") if l.strip()][:20]
    if "achievements" in sections:
        resume.achievements = [l.strip("-• \t") for l in sections["achievements"].split("\n") if l.strip()][:20]

    # Best-effort name guess: first non-empty line if it looks like a name (short, no @ or digits)
    for line in text.split("\n"):
        candidate = line.strip()
        if candidate and "@" not in candidate and not any(c.isdigit() for c in candidate) and len(candidate.split()) <= 5:
            resume.name = candidate
            break

    return resume
