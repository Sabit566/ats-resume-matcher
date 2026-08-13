"""
Job category detection and category-specific scoring weights.
Supports matching across all major industries and role types.
"""

import re
from typing import Dict, List, Tuple

JOB_CATEGORIES = [
    "Technology",
    "Healthcare",
    "Finance",
    "Sales & Marketing",
    "Design & Creative",
    "Operations & HR",
    "Legal",
    "Education & Research",
    "Trades & Engineering",
    "General",
]

# Keywords and title hints used to score each category from JD/resume text.
CATEGORY_SIGNALS: Dict[str, Dict[str, List[str]]] = {
    "Technology": {
        "keywords": [
            "software", "developer", "engineer", "programming", "python", "java",
            "javascript", "cloud", "devops", "api", "database", "machine learning",
            "frontend", "backend", "full stack", "agile", "scrum", "kubernetes",
            "aws", "react", "node.js", "data scientist", "cybersecurity",
        ],
        "titles": [
            "software engineer", "developer", "devops", "data scientist",
            "full stack", "backend engineer", "frontend engineer", "sre",
            "machine learning engineer", "qa engineer", "product engineer",
        ],
    },
    "Healthcare": {
        "keywords": [
            "patient", "clinical", "nursing", "medical", "hospital", "healthcare",
            "physician", "doctor", "pharmacy", "diagnosis", "treatment", "emr",
            "ehr", "hipaa", "icu", "surgery", "radiology", "laboratory",
            "registered nurse", "rn", "lpn", "cna", "phlebotomy", "telehealth",
        ],
        "titles": [
            "registered nurse", "nurse", "physician", "doctor", "pharmacist",
            "medical assistant", "clinical", "healthcare", "therapist",
            "radiologist", "lab technician", "care coordinator",
        ],
    },
    "Finance": {
        "keywords": [
            "accounting", "finance", "audit", "tax", "cpa", "cfa", "investment",
            "banking", "financial", "budget", "forecast", "reconciliation",
            "gaap", "ifrs", "portfolio", "risk management", "compliance",
            "bookkeeping", "accounts payable", "accounts receivable", "fp&a",
        ],
        "titles": [
            "accountant", "financial analyst", "auditor", "controller",
            "investment banker", "financial advisor", "bookkeeper",
            "tax specialist", "credit analyst", "treasury analyst",
        ],
    },
    "Sales & Marketing": {
        "keywords": [
            "sales", "marketing", "crm", "lead generation", "campaign",
            "brand", "seo", "sem", "social media", "content marketing",
            "b2b", "b2c", "quota", "pipeline", "conversion", "advertising",
            "hubspot", "salesforce", "google ads", "email marketing", "copywriting",
        ],
        "titles": [
            "sales representative", "account executive", "marketing manager",
            "digital marketer", "brand manager", "business development",
            "sales manager", "marketing specialist", "content strategist",
        ],
    },
    "Design & Creative": {
        "keywords": [
            "design", "ui", "ux", "figma", "adobe", "photoshop", "illustrator",
            "creative", "branding", "typography", "wireframe", "prototype",
            "visual design", "graphic design", "motion graphics", "portfolio",
            "invision", "sketch", "canva", "video editing", "animation",
        ],
        "titles": [
            "graphic designer", "ui designer", "ux designer", "product designer",
            "creative director", "art director", "visual designer", "illustrator",
            "motion designer", "web designer",
        ],
    },
    "Operations & HR": {
        "keywords": [
            "operations", "human resources", "hr", "recruiting", "talent",
            "payroll", "onboarding", "employee relations", "supply chain",
            "logistics", "inventory", "procurement", "vendor management",
            "process improvement", "workday", "bamboohr", "ats", "hris",
        ],
        "titles": [
            "hr manager", "recruiter", "operations manager", "supply chain",
            "logistics coordinator", "office manager", "talent acquisition",
            "people operations", "hr generalist", "business operations",
        ],
    },
    "Legal": {
        "keywords": [
            "legal", "law", "attorney", "litigation", "contract", "compliance",
            "regulatory", "paralegal", "court", "bar admission", "due diligence",
            "intellectual property", "corporate law", "legal research",
        ],
        "titles": [
            "attorney", "lawyer", "paralegal", "legal counsel", "legal assistant",
            "compliance officer", "contract manager", "legal analyst",
        ],
    },
    "Education & Research": {
        "keywords": [
            "teaching", "research", "academic", "university", "curriculum",
            "publication", "grant", "phd", "professor", "lecturer", "student",
            "classroom", "education", "scholarly", "thesis", "laboratory research",
        ],
        "titles": [
            "teacher", "professor", "researcher", "research scientist",
            "lecturer", "instructor", "teaching assistant", "postdoctoral",
            "academic advisor", "principal",
        ],
    },
    "Trades & Engineering": {
        "keywords": [
            "mechanical", "electrical", "civil", "construction", "manufacturing",
            "hvac", "plumbing", "welding", "cad", "autocad", "blueprint",
            "maintenance", "technician", "safety", "osha", "quality control",
            "industrial", "cnc", "fabrication", "site supervisor",
        ],
        "titles": [
            "mechanical engineer", "electrical engineer", "civil engineer",
            "technician", "maintenance", "project engineer", "site supervisor",
            "quality inspector", "fabricator", "electrician", "plumber",
        ],
    },
}

DEFAULT_WEIGHTS = {
    "semantic": 0.35,
    "skills": 0.25,
    "experience": 0.20,
    "education": 0.10,
    "keyword": 0.10,
}

CATEGORY_WEIGHTS: Dict[str, Dict[str, float]] = {
    "Technology": {"semantic": 0.30, "skills": 0.35, "experience": 0.15, "education": 0.08, "keyword": 0.12},
    "Healthcare": {"semantic": 0.25, "skills": 0.30, "experience": 0.20, "education": 0.15, "keyword": 0.10},
    "Finance": {"semantic": 0.28, "skills": 0.22, "experience": 0.22, "education": 0.18, "keyword": 0.10},
    "Sales & Marketing": {"semantic": 0.35, "skills": 0.20, "experience": 0.25, "education": 0.05, "keyword": 0.15},
    "Design & Creative": {"semantic": 0.30, "skills": 0.30, "experience": 0.20, "education": 0.05, "keyword": 0.15},
    "Operations & HR": {"semantic": 0.32, "skills": 0.22, "experience": 0.25, "education": 0.08, "keyword": 0.13},
    "Legal": {"semantic": 0.25, "skills": 0.20, "experience": 0.20, "education": 0.25, "keyword": 0.10},
    "Education & Research": {"semantic": 0.28, "skills": 0.18, "experience": 0.18, "education": 0.26, "keyword": 0.10},
    "Trades & Engineering": {"semantic": 0.22, "skills": 0.35, "experience": 0.28, "education": 0.08, "keyword": 0.07},
    "General": DEFAULT_WEIGHTS,
}


def _score_category(text: str, signals: Dict[str, List[str]]) -> float:
    lower = text.lower()
    score = 0.0
    for kw in signals.get("keywords", []):
        if kw in lower:
            score += 1.0
    for title in signals.get("titles", []):
        if title in lower:
            score += 2.0
    return score


def detect_job_category(jd_text: str, resume_text: str = "") -> Tuple[str, Dict[str, float]]:
    """Detect the most likely job category from JD (primary) and resume (secondary)."""
    combined = f"{jd_text}\n{resume_text}"
    scores = {cat: _score_category(combined, CATEGORY_SIGNALS[cat]) for cat in JOB_CATEGORIES if cat != "General"}

    best_cat = max(scores, key=scores.get) if scores else "General"
    if scores.get(best_cat, 0) < 2.0:
        best_cat = "General"

    return best_cat, scores


def weights_for_category(category: str) -> Dict[str, float]:
    return CATEGORY_WEIGHTS.get(category, DEFAULT_WEIGHTS)
