"""
Semantic similarity between resume and job description.

The original spec calls for Sentence-Transformer embeddings
(all-MiniLM-L6-v2 / all-mpnet-base-v2 / bge-base-en-v1.5). Those models are
downloaded from Hugging Face at runtime, which requires an internet
connection to huggingface.co. This module is written so that swapping in
real embeddings is a one-function change (see `_embed_with_sentence_transformers`
below) — if you run this project on a machine with internet access, install
`sentence-transformers` and flip `USE_SENTENCE_TRANSFORMERS = True`.

Until then, we fall back to a strong TF-IDF + cosine-similarity signal
(scikit-learn), which is a reasonable proxy for lexical/semantic overlap
and needs no external downloads.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

USE_SENTENCE_TRANSFORMERS = False
_st_model = None


def _embed_with_sentence_transformers(resume_text: str, jd_text: str) -> float:
    global _st_model
    from sentence_transformers import SentenceTransformer, util

    if _st_model is None:
        _st_model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = _st_model.encode([resume_text, jd_text])
    sim = util.cos_sim(embeddings[0], embeddings[1]).item()
    return max(0.0, min(1.0, sim))


def _tfidf_similarity(resume_text: str, jd_text: str) -> float:
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        tfidf = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:
        return 0.0
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return max(0.0, min(1.0, sim))


def semantic_similarity(resume_text: str, jd_text: str) -> dict:
    if USE_SENTENCE_TRANSFORMERS:
        try:
            sim = _embed_with_sentence_transformers(resume_text, jd_text)
            method = "sentence-transformers (all-MiniLM-L6-v2)"
        except Exception:
            sim = _tfidf_similarity(resume_text, jd_text)
            method = "tfidf-cosine (fallback)"
    else:
        sim = _tfidf_similarity(resume_text, jd_text)
        method = "tfidf-cosine"

    return {"score": round(sim * 100, 1), "method": method}
