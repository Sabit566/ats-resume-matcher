from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from resume_parser import parse_resume
from jd_parser import parse_job_description
from skill_matcher import match_skills
from semantic_matcher import semantic_similarity
from experience_matcher import match_experience
from education_matcher import match_education
from keyword_matcher import keyword_coverage
from score_engine import compute_overall_score
from report_generator import build_report
from job_categories import detect_job_category

app = FastAPI(title="ATS Resume Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")


@app.post("/api/match")
async def match_resume(
    jd_text: str = Form(...),
    resume_file: UploadFile = File(None),
    resume_text: str = Form(""),
):
    if resume_file is not None:
        content = await resume_file.read()
        resume_meta = parse_resume(resume_file.filename, content)
    else:
        resume_meta = {
            "raw_text": resume_text,
            "name": "",
            "email": "",
            "phone": "",
            "sections": {},
        }

    jd_meta = parse_job_description(jd_text)

    r_text = resume_meta["raw_text"]
    j_text = jd_meta["raw_text"]
    sections = resume_meta.get("sections", {})

    job_category, category_scores = detect_job_category(j_text, r_text)

    semantic_result = semantic_similarity(r_text, j_text)
    skill_result = match_skills(
        r_text, j_text,
        required_block=jd_meta.get("required_block", ""),
        preferred_block=jd_meta.get("preferred_block", ""),
    )
    experience_result = match_experience(
        r_text, j_text,
        jd_years_hint=jd_meta.get("required_years", 0.0),
    )
    education_result = match_education(
        r_text, j_text,
        jd_level_hint=jd_meta.get("required_education_level", 0),
        resume_sections=sections,
    )
    keyword_result = keyword_coverage(
        r_text, j_text,
        required_block=jd_meta.get("required_block", ""),
        resume_sections=sections,
    )

    score_result = compute_overall_score(
        semantic_result["score"],
        skill_result["score"],
        experience_result["score"],
        education_result["score"],
        keyword_result["score"],
        job_category=job_category,
    )

    report = build_report(
        semantic_result, skill_result, experience_result,
        education_result, keyword_result, score_result, resume_meta,
        job_category=job_category,
        category_scores=category_scores,
        jd_meta=jd_meta,
    )
    return report


@app.get("/api/health")
def health():
    return {"status": "ok"}


if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
