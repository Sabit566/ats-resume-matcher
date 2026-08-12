"""
Central skill taxonomy + synonym dictionary for the ATS Resume Matcher.
"""

SKILL_CATEGORIES = {
    "Programming": ["Python", "Java", "C#", "JavaScript", "TypeScript", "Go", "Rust", "C++"],
    "Frontend": ["React", "Angular", "Vue", "Next.js", "HTML", "CSS", "Tailwind CSS", "Redux"],
    "Backend": ["Node.js", "Express", "Spring Boot", ".NET", "Django", "Flask", "FastAPI"],
    "Cloud": ["AWS", "Azure", "Google Cloud Platform", "GCP"],
    "DevOps": ["Docker", "Kubernetes", "Terraform", "Jenkins", "GitHub Actions", "Ansible", "CI/CD"],
    "Database": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite", "Oracle"],
    "AI": ["TensorFlow", "PyTorch", "OpenAI", "LangChain", "RAG", "LLMs", "Scikit-learn",
           "Machine Learning", "Artificial Intelligence", "NLP", "Pandas", "NumPy"],
    "Monitoring": ["Prometheus", "Grafana", "Datadog", "New Relic"],
    "Messaging": ["Kafka", "RabbitMQ", "SQS"],
}

# Canonical term -> list of alternate surface forms found in text.
SYNONYMS = {
    "Node.js": ["Node", "NodeJS"],
    "JavaScript": ["JS"],
    "TypeScript": ["TS"],
    "Kubernetes": ["K8s"],
    "Google Cloud Platform": ["GCP"],
    "REST API": ["RESTful API", "REST APIs", "RESTful APIs"],
    "Microservices": ["Microservice Architecture", "Microservice"],
    "CI/CD": ["Continuous Integration", "Continuous Integration/Continuous Deployment",
              "Continuous Deployment"],
    "Cloud-Native": ["Cloud Native"],
    "Artificial Intelligence": ["AI"],
    "Machine Learning": ["ML"],
    ".NET": ["DotNet", "dotnet"],
    "HTML": ["HTML5"],
    "CSS": ["CSS3"],
}

# Build a flat lookup: any surface form (lowercased) -> canonical name
def _build_lookup():
    lookup = {}
    all_terms = set()
    for terms in SKILL_CATEGORIES.values():
        all_terms.update(terms)
    for canon, alts in SYNONYMS.items():
        all_terms.add(canon)
        all_terms.update(alts)

    for term in all_terms:
        lookup[term.lower()] = term

    for canon, alts in SYNONYMS.items():
        canon_norm = lookup.get(canon.lower(), canon)
        for alt in alts:
            lookup[alt.lower()] = canon_norm
    return lookup


SURFACE_TO_CANONICAL = _build_lookup()

# Flat list of all canonical + alt forms, sorted longest-first so multi-word
# skills (e.g. "Google Cloud Platform") are matched before short ones (e.g. "GCP").
ALL_SURFACE_FORMS = sorted(SURFACE_TO_CANONICAL.keys(), key=len, reverse=True)


def canonical_category(canon_name: str) -> str:
    for cat, terms in SKILL_CATEGORIES.items():
        if canon_name in terms:
            return cat
    return "Other"
