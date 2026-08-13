"""
Skills taxonomy, categories, and synonym normalization for the ATS matcher.
"""

# Canonical skill -> category
SKILLS_TAXONOMY = {
    # Programming
    "python": "Programming",
    "java": "Programming",
    "c#": "Programming",
    "javascript": "Programming",
    "typescript": "Programming",
    "go": "Programming",
    "rust": "Programming",
    "c++": "Programming",
    "php": "Programming",
    "ruby": "Programming",

    # Frontend
    "react": "Frontend",
    "angular": "Frontend",
    "vue": "Frontend",
    "next.js": "Frontend",
    "html": "Frontend",
    "css": "Frontend",
    "tailwind css": "Frontend",
    "redux": "Frontend",

    # Backend
    "node.js": "Backend",
    "express": "Backend",
    "spring boot": "Backend",
    ".net": "Backend",
    "django": "Backend",
    "flask": "Backend",
    "fastapi": "Backend",

    # Cloud
    "aws": "Cloud",
    "azure": "Cloud",
    "google cloud platform": "Cloud",

    # DevOps
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "terraform": "DevOps",
    "jenkins": "DevOps",
    "github actions": "DevOps",
    "ansible": "DevOps",
    "ci/cd": "DevOps",

    # Database
    "mysql": "Database",
    "postgresql": "Database",
    "mongodb": "Database",
    "redis": "Database",
    "elasticsearch": "Database",
    "sqlite": "Database",

    # AI
    "tensorflow": "AI",
    "pytorch": "AI",
    "openai": "AI",
    "langchain": "AI",
    "rag": "AI",
    "llms": "AI",
    "scikit-learn": "AI",
    "spacy": "AI",
    "nlp": "AI",
    "machine learning": "AI",
    "artificial intelligence": "AI",

    # Monitoring (used by report examples)
    "prometheus": "Monitoring",
    "grafana": "Monitoring",

    # Architecture / other
    "rest api": "Architecture",
    "microservices": "Architecture",
    "cloud-native": "Architecture",
    "kafka": "Backend",
    "graphql": "Backend",
}

# Synonym -> canonical form. Keys and values are lowercase.
SYNONYMS = {
    "node": "node.js",
    "nodejs": "node.js",
    "js": "javascript",
    "ts": "typescript",
    "k8s": "kubernetes",
    "gcp": "google cloud platform",
    "google cloud": "google cloud platform",
    "restful api": "rest api",
    "rest apis": "rest api",
    "restful apis": "rest api",
    "microservice architecture": "microservices",
    "microservice": "microservices",
    "cloud native": "cloud-native",
    "continuous integration": "ci/cd",
    "continuous integration / continuous deployment": "ci/cd",
    "continuous deployment": "ci/cd",
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "nextjs": "next.js",
    "next": "next.js",
    "dotnet": ".net",
    "asp.net": ".net",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "es": "elasticsearch",
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "large language models": "llms",
    "llm": "llms",
    "retrieval augmented generation": "rag",
    "retrieval-augmented generation": "rag",
    "spring": "spring boot",
    "actions": "github actions",
    "gh actions": "github actions",
}

DEGREE_LEVELS = {
    "phd": 3,
    "ph.d": 3,
    "ph.d.": 3,
    "doctorate": 3,
    "doctor of philosophy": 3,
    "master": 2,
    "masters": 2,
    "master's": 2,
    "msc": 2,
    "m.sc": 2,
    "ms": 2,
    "m.s.": 2,
    "mba": 2,
    "bachelor": 1,
    "bachelors": 1,
    "bachelor's": 1,
    "bsc": 1,
    "b.sc": 1,
    "bs": 1,
    "b.s.": 1,
    "b.tech": 1,
    "btech": 1,
    "be": 1,
    "b.e.": 1,
}

TITLE_EQUIVALENCE_GROUPS = [
    ["principal software engineer", "lead software engineer", "senior software engineer",
     "engineering lead", "staff software engineer", "software architect"],
    ["software engineer", "swe", "developer", "programmer", "software developer"],
    ["data scientist", "machine learning engineer", "ml engineer", "ai engineer"],
    ["engineering manager", "team lead", "tech lead", "technical lead"],
    ["product manager", "senior product manager", "product owner"],
]


def normalize_term(term: str) -> str:
    """Lowercase and map a raw term to its canonical skill name if a synonym exists."""
    t = term.strip().lower()
    return SYNONYMS.get(t, t)


def category_for(skill: str) -> str:
    return SKILLS_TAXONOMY.get(normalize_term(skill), "Other")


ALL_KNOWN_SKILLS = sorted(set(SKILLS_TAXONOMY.keys()) | set(SYNONYMS.keys()))
