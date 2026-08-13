"""
Central skill taxonomy + synonym dictionary for all job categories.
Covers technology, healthcare, finance, sales, design, operations, legal,
education, trades, and general professional skills.
"""

SKILL_CATEGORIES = {
    # Technology
    "Programming": [
        "Python", "Java", "C#", "JavaScript", "TypeScript", "Go", "Rust", "C++",
        "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "MATLAB",
    ],
    "Frontend": [
        "React", "Angular", "Vue", "Next.js", "HTML", "CSS", "Tailwind CSS",
        "Redux", "Svelte", "Bootstrap", "jQuery",
    ],
    "Backend": [
        "Node.js", "Express", "Spring Boot", ".NET", "Django", "Flask", "FastAPI",
        "GraphQL", "REST API", "Microservices", "Kafka", "RabbitMQ",
    ],
    "Cloud": ["AWS", "Azure", "Google Cloud Platform", "GCP", "Cloud-Native"],
    "DevOps": [
        "Docker", "Kubernetes", "Terraform", "Jenkins", "GitHub Actions",
        "Ansible", "CI/CD", "Git", "Linux",
    ],
    "Database": [
        "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch", "SQLite",
        "Oracle", "SQL Server", "DynamoDB", "Snowflake",
    ],
    "AI & Data": [
        "TensorFlow", "PyTorch", "OpenAI", "LangChain", "RAG", "LLMs",
        "Scikit-learn", "Machine Learning", "Artificial Intelligence", "NLP",
        "Pandas", "NumPy", "Data Analysis", "Power BI", "Tableau", "Spark",
        "Hadoop", "ETL", "Data Warehousing",
    ],
    "Monitoring": ["Prometheus", "Grafana", "Datadog", "New Relic", "Splunk"],
    "Cybersecurity": [
        "Cybersecurity", "Penetration Testing", "SIEM", "Firewall",
        "ISO 27001", "SOC 2", "Identity Management",
    ],

    # Healthcare
    "Clinical": [
        "Patient Care", "Clinical Assessment", "Diagnosis", "Treatment Planning",
        "Electronic Health Records", "EHR", "EMR", "HIPAA", "Medical Coding",
        "ICD-10", "CPT Coding", "Telehealth", "Triage", "Vital Signs",
    ],
    "Medical Specialties": [
        "Nursing", "Pharmacy", "Radiology", "Laboratory", "Surgery",
        "Physical Therapy", "Occupational Therapy", "Mental Health",
        "Pediatrics", "Emergency Medicine", "ICU", "Anesthesia",
    ],
    "Healthcare Certs": [
        "RN", "LPN", "CNA", "BLS", "ACLS", "PALS", "CPR", "NP",
        "Medical License", "Board Certification",
    ],

    # Finance
    "Accounting": [
        "Accounting", "Bookkeeping", "General Ledger", "Accounts Payable",
        "Accounts Receivable", "Financial Reporting", "Reconciliation",
        "GAAP", "IFRS", "Tax Preparation", "Audit",
    ],
    "Finance Tools": [
        "QuickBooks", "SAP", "Oracle Financials", "Excel", "Financial Modeling",
        "Budgeting", "Forecasting", "FP&A", "Variance Analysis",
    ],
    "Finance Certs": ["CPA", "CFA", "CMA", "FRM", "CIA", "Series 7", "Series 63"],
    "Banking & Investment": [
        "Investment Banking", "Portfolio Management", "Risk Management",
        "Credit Analysis", "Treasury", "Compliance", "Anti-Money Laundering",
        "KYC", "Due Diligence",
    ],

    # Sales & Marketing
    "Sales": [
        "Sales", "Lead Generation", "Pipeline Management", "CRM", "Salesforce",
        "HubSpot", "B2B Sales", "B2C Sales", "Account Management",
        "Negotiation", "Cold Calling", "Prospecting", "Closing",
    ],
    "Marketing": [
        "Digital Marketing", "SEO", "SEM", "Content Marketing", "Email Marketing",
        "Social Media Marketing", "Brand Management", "Market Research",
        "Google Ads", "Facebook Ads", "Analytics", "Google Analytics",
        "Copywriting", "Campaign Management", "Marketing Automation",
    ],

    # Design & Creative
    "Design Tools": [
        "Figma", "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign",
        "Sketch", "Canva", "InVision", "Adobe XD", "After Effects",
        "Premiere Pro", "Blender", "3D Modeling",
    ],
    "Design Skills": [
        "UI Design", "UX Design", "Graphic Design", "Visual Design",
        "Wireframing", "Prototyping", "Typography", "Branding",
        "Motion Graphics", "Video Editing", "Photography",
    ],

    # Operations & HR
    "HR": [
        "Human Resources", "Recruiting", "Talent Acquisition", "Onboarding",
        "Employee Relations", "Payroll", "Benefits Administration",
        "Performance Management", "Workday", "BambooHR", "HRIS", "ATS",
    ],
    "Operations": [
        "Operations Management", "Supply Chain", "Logistics", "Inventory Management",
        "Procurement", "Vendor Management", "Process Improvement", "Lean",
        "Six Sigma", "Project Management", "Agile", "Scrum", "Kanban",
    ],

    # Legal
    "Legal Skills": [
        "Legal Research", "Contract Law", "Litigation", "Compliance",
        "Regulatory Affairs", "Intellectual Property", "Corporate Law",
        "Due Diligence", "Legal Writing", "Case Management",
    ],
    "Legal Certs": ["Bar Admission", "Paralegal Certification", "Notary Public"],

    # Education & Research
    "Education": [
        "Teaching", "Curriculum Development", "Classroom Management",
        "Student Assessment", "Lesson Planning", "Educational Technology",
        "LMS", "Moodle", "Blackboard", "Canvas LMS",
    ],
    "Research": [
        "Research", "Academic Writing", "Grant Writing", "Statistical Analysis",
        "Literature Review", "Peer Review", "Laboratory Research",
        "Qualitative Research", "Quantitative Research",
    ],

    # Trades & Engineering
    "Engineering": [
        "Mechanical Engineering", "Electrical Engineering", "Civil Engineering",
        "Structural Engineering", "CAD", "AutoCAD", "SolidWorks", "Revit",
        "Quality Control", "Manufacturing", "CNC", "Blueprint Reading",
    ],
    "Trades": [
        "HVAC", "Plumbing", "Welding", "Electrical Work", "Construction",
        "Maintenance", "Fabrication", "OSHA", "Safety Compliance",
        "Equipment Operation", "Forklift", "Site Supervision",
    ],

    # General professional
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management", "Presentation Skills",
        "Customer Service", "Conflict Resolution", "Adaptability",
    ],
    "Office & Productivity": [
        "Microsoft Office", "Microsoft Excel", "Microsoft Word", "Microsoft PowerPoint",
        "Google Workspace", "Slack", "Zoom", "Notion", "Jira", "Confluence",
    ],
    "Languages": [
        "English", "Spanish", "French", "German", "Mandarin", "Arabic",
        "Bilingual", "Multilingual",
    ],
}

SYNONYMS = {
    # Tech
    "Node.js": ["Node", "NodeJS"],
    "JavaScript": ["JS"],
    "TypeScript": ["TS"],
    "Kubernetes": ["K8s"],
    "Google Cloud Platform": ["GCP", "Google Cloud"],
    "REST API": ["RESTful API", "REST APIs", "RESTful APIs"],
    "Microservices": ["Microservice Architecture", "Microservice"],
    "CI/CD": ["Continuous Integration", "Continuous Integration/Continuous Deployment",
              "Continuous Deployment"],
    "Cloud-Native": ["Cloud Native"],
    "Artificial Intelligence": ["AI"],
    "Machine Learning": ["ML"],
    ".NET": ["DotNet", "dotnet", "ASP.NET"],
    "HTML": ["HTML5"],
    "CSS": ["CSS3"],
    "PostgreSQL": ["Postgres"],
    "MongoDB": ["Mongo"],
    "Elasticsearch": ["ES"],
    "Scikit-learn": ["Sklearn"],
    "LLMs": ["LLM", "Large Language Models"],
    "RAG": ["Retrieval Augmented Generation", "Retrieval-Augmented Generation"],
    "Next.js": ["NextJS", "Next"],
    "GitHub Actions": ["GH Actions"],
    "Spring Boot": ["Spring"],
    "Electronic Health Records": ["EHR"],
    "EMR": ["Electronic Medical Records"],

    # Healthcare
    "RN": ["Registered Nurse"],
    "LPN": ["Licensed Practical Nurse"],
    "CNA": ["Certified Nursing Assistant"],
    "ICU": ["Intensive Care Unit"],
    "HIPAA": ["Health Insurance Portability and Accountability Act"],

    # Finance
    "FP&A": ["Financial Planning and Analysis"],
    "GAAP": ["Generally Accepted Accounting Principles"],
    "KYC": ["Know Your Customer"],
    "Anti-Money Laundering": ["AML"],

    # Marketing
    "SEO": ["Search Engine Optimization"],
    "SEM": ["Search Engine Marketing"],
    "Google Analytics": ["GA4"],

    # Design
    "UI Design": ["User Interface Design"],
    "UX Design": ["User Experience Design"],
    "Adobe Photoshop": ["Photoshop"],
    "Adobe Illustrator": ["Illustrator"],
    "Adobe InDesign": ["InDesign"],
    "Adobe XD": ["XD"],

    # General
    "Microsoft Excel": ["Excel", "MS Excel"],
    "Microsoft Word": ["Word", "MS Word"],
    "Microsoft PowerPoint": ["PowerPoint", "PPT"],
    "Microsoft Office": ["MS Office", "Office 365"],
    "Human Resources": ["HR"],
    "Project Management": ["PM"],
    "Customer Service": ["Client Service"],
    "Supply Chain": ["SCM", "Supply Chain Management"],
    "Six Sigma": ["6 Sigma"],
    "Quality Control": ["QC"],
    "Computer Numerical Control": ["CNC"],
}


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
ALL_SURFACE_FORMS = sorted(SURFACE_TO_CANONICAL.keys(), key=len, reverse=True)


def canonical_category(canon_name: str) -> str:
    for cat, terms in SKILL_CATEGORIES.items():
        if canon_name in terms:
            return cat
    return "Other"


def all_canonical_skills() -> list:
    skills = set()
    for terms in SKILL_CATEGORIES.values():
        skills.update(terms)
    return sorted(skills)
