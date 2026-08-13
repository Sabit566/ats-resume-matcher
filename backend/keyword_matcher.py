import re
from sklearn.feature_extraction.text import TfidfVectorizer

GENERIC_STOPWORDS = {
    "experience", "years", "work", "role", "team", "company", "job", "position",
    "ability", "skills", "required", "preferred", "qualifications", "responsibilities",
    "including", "using", "working", "strong", "excellent", "good", "well",
    "must", "have", "will", "able", "within", "across", "various", "related",
    "candidate", "applicants", "apply", "opportunity", "join", "looking",
}


def _tokenize(text: str) -> set:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9\+\#\.]{1,}", text.lower())
    return {w for w in words if w not in GENERIC_STOPWORDS and len(w) > 2}


def _section_boost_tokens(resume_sections: dict) -> set:
    """Give extra weight to skills/experience sections when checking coverage."""
    tokens = set()
    priority_sections = ["skills", "technical skills", "experience",
                           "work experience", "professional experience", "summary"]
    for section in priority_sections:
        if section in resume_sections and resume_sections[section]:
            tokens.update(_tokenize(resume_sections[section]))
    return tokens


def keyword_coverage(
    resume_text: str,
    jd_text: str,
    required_block: str = "",
    resume_sections: dict = None,
) -> dict:
    """Measure how many important JD keywords appear in the resume."""
    jd_source = required_block.strip() or jd_text
    if not jd_source.strip():
        return {"score": 100.0, "top_keywords": [], "covered_keywords": [], "missing_keywords": []}

    vectorizer = TfidfVectorizer(stop_words="english", max_features=40, ngram_range=(1, 2))
    try:
        vectorizer.fit([jd_source])
    except ValueError:
        return {"score": 0.0, "top_keywords": [], "covered_keywords": [], "missing_keywords": []}

    top_keywords = [kw for kw in vectorizer.get_feature_names_out().tolist()
                    if kw not in GENERIC_STOPWORDS]
    resume_tokens = _tokenize(resume_text)
    if resume_sections:
        resume_tokens |= _section_boost_tokens(resume_sections)

    covered = [kw for kw in top_keywords if kw in resume_tokens]
    missing = [kw for kw in top_keywords if kw not in resume_tokens]
    score = round(len(covered) / len(top_keywords) * 100, 1) if top_keywords else 100.0

    return {
        "score": score,
        "top_keywords": top_keywords,
        "covered_keywords": covered,
        "missing_keywords": missing,
    }
