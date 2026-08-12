from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from resume_parser import parse_resume
from jd_parser import parse_job_description
from skill_matcher import match_skills
from semantic_matcher import semantic_similarity
from experience_matcher import match_experience
from education_matcher import match_education
from keyword_matcher import keyword_coverage
from score_engine import compute_overall_score
from report_generator import build_report

app = FastAPI(title="ATS Resume Matcher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    semantic_result = semantic_similarity(r_text, j_text)
    skill_result = match_skills(r_text, j_text)
    experience_result = match_experience(r_text, j_text)
    education_result = match_education(r_text, j_text)
    keyword_result = keyword_coverage(r_text, j_text)

    score_result = compute_overall_score(
        semantic_result["score"],
        skill_result["score"],
        experience_result["score"],
        education_result["score"],
        keyword_result["score"],
    )

    report = build_report(
        semantic_result, skill_result, experience_result,
        education_result, keyword_result, score_result, resume_meta,
    )
    return report


@app.get("/api/health")
def health():
    return {"status": "ok"}
