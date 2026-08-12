import re
import io


EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}")

SECTION_HEADERS = [
    "experience", "work experience", "professional experience",
    "education", "skills", "technical skills", "projects",
    "certifications", "achievements", "summary", "objective",
]


def extract_text_from_bytes(filename: str, content: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return _extract_pdf(content)
    if lower.endswith(".docx"):
        return _extract_docx(content)
    # plain text / fallback
    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def _extract_pdf(content: bytes) -> str:
    import pdfplumber
    text_parts = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text_parts.append(page_text)
    return "\n".join(text_parts)


def _extract_docx(content: bytes) -> str:
    import docx
    doc = docx.Document(io.BytesIO(content))
    return "\n".join(p.text for p in doc.paragraphs)


def _guess_name(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines[:5]:
        if EMAIL_RE.search(line) or PHONE_RE.search(line):
            continue
        if len(line.split()) <= 5 and not any(ch.isdigit() for ch in line):
            return line
    return ""


def _split_sections(text: str) -> dict:
    lines = text.splitlines()
    sections = {}
    current = "header"
    buffer = []
    for line in lines:
        clean = line.strip().lower().rstrip(":")
        matched_header = next((h for h in SECTION_HEADERS if clean == h), None)
        if matched_header:
            sections[current] = "\n".join(buffer).strip()
            current = matched_header
            buffer = []
        else:
            buffer.append(line)
    sections[current] = "\n".join(buffer).strip()
    return sections


def parse_resume(filename: str, content: bytes) -> dict:
    text = extract_text_from_bytes(filename, content)
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)
    sections = _split_sections(text)

    return {
        "raw_text": text,
        "name": _guess_name(text),
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
        "sections": sections,
    }
