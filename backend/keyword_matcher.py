import re
from sklearn.feature_extraction.text import TfidfVectorizer

STOPWORD_EXTRA = {"experience", "years", "work", "role", "team", "company", "job"}


def _tokenize(text: str) -> set:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9\+\#\.]{1,}", text.lower())
    return {w for w in words if w not in STOPWORD_EXTRA and len(w) > 2}


def keyword_coverage(resume_text: str, jd_text: str) -> dict:
    """Weight JD keywords by TF-IDF importance, then measure how many
    of the top keywords appear in the resume (a BM25/TF-IDF style
    lexical coverage score)."""
    if not jd_text.strip():
        return {"score": 100.0, "top_keywords": [], "covered_keywords": []}

    vectorizer = TfidfVectorizer(stop_words="english", max_features=30)
    try:
        vectorizer.fit([jd_text])
    except ValueError:
        return {"score": 0.0, "top_keywords": [], "covered_keywords": []}

    top_keywords = vectorizer.get_feature_names_out().tolist()
    resume_tokens = _tokenize(resume_text)

    covered = [kw for kw in top_keywords if kw in resume_tokens]
    score = round(len(covered) / len(top_keywords) * 100, 1) if top_keywords else 100.0

    return {
        "score": score,
        "top_keywords": top_keywords,
        "covered_keywords": covered,
    }
