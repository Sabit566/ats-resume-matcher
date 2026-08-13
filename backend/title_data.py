"""
Title equivalence groups across all job categories.
Used by experience_matcher to compare resume titles against JD requirements.
"""

TITLE_GROUPS = [
    # Technology
    ["Principal Software Engineer", "Lead Software Engineer", "Senior Software Engineer",
     "Engineering Lead", "Staff Software Engineer", "Software Architect"],
    ["Software Engineer", "Software Developer", "Backend Engineer", "Frontend Engineer",
     "Full Stack Engineer", "Full Stack Developer", "Web Developer", "Programmer"],
    ["Data Scientist", "Machine Learning Engineer", "ML Engineer", "AI Engineer",
     "Data Analyst", "Business Intelligence Analyst"],
    ["Engineering Manager", "Technical Lead", "Tech Lead", "Team Lead", "Development Manager"],
    ["DevOps Engineer", "Site Reliability Engineer", "SRE", "Cloud Engineer",
     "Platform Engineer", "Infrastructure Engineer"],
    ["QA Engineer", "Quality Assurance Engineer", "Test Engineer", "SDET"],
    ["Product Manager", "Senior Product Manager", "Product Owner", "Technical Product Manager"],
    ["Cybersecurity Analyst", "Security Engineer", "Information Security Analyst"],

    # Healthcare
    ["Registered Nurse", "RN", "Staff Nurse", "Clinical Nurse"],
    ["Licensed Practical Nurse", "LPN", "LVN"],
    ["Certified Nursing Assistant", "CNA", "Nursing Assistant"],
    ["Physician", "Doctor", "Medical Doctor", "MD"],
    ["Nurse Practitioner", "NP", "Advanced Practice Nurse"],
    ["Pharmacist", "Clinical Pharmacist", "Pharmacy Technician"],
    ["Medical Assistant", "Clinical Assistant", "Healthcare Assistant"],
    ["Physical Therapist", "PT", "Occupational Therapist", "OT"],
    ["Radiologic Technologist", "Radiology Technician", "X-Ray Technician"],
    ["Lab Technician", "Medical Laboratory Technician", "Phlebotomist"],
    ["Healthcare Administrator", "Hospital Administrator", "Clinical Coordinator"],

    # Finance
    ["Accountant", "Staff Accountant", "Senior Accountant", "Accounting Clerk"],
    ["Financial Analyst", "Senior Financial Analyst", "Finance Analyst"],
    ["Auditor", "Internal Auditor", "External Auditor", "Audit Manager"],
    ["Controller", "Financial Controller", "Assistant Controller"],
    ["Bookkeeper", "Accounting Specialist", "Accounts Payable Specialist"],
    ["Investment Banker", "Investment Analyst", "Portfolio Manager"],
    ["Tax Specialist", "Tax Accountant", "Tax Preparer"],
    ["Credit Analyst", "Risk Analyst", "Compliance Analyst"],
    ["Treasury Analyst", "Cash Management Specialist"],

    # Sales & Marketing
    ["Sales Representative", "Sales Rep", "Account Executive", "Sales Associate"],
    ["Sales Manager", "Regional Sales Manager", "Sales Director"],
    ["Business Development Representative", "BDR", "SDR", "Sales Development Representative"],
    ["Marketing Manager", "Marketing Specialist", "Marketing Coordinator"],
    ["Digital Marketing Manager", "Digital Marketer", "Online Marketing Specialist"],
    ["Content Marketing Manager", "Content Strategist", "Copywriter"],
    ["Brand Manager", "Brand Strategist", "Brand Marketing Manager"],
    ["SEO Specialist", "SEO Manager", "Search Engine Optimization Specialist"],
    ["Social Media Manager", "Social Media Specialist", "Community Manager"],

    # Design & Creative
    ["Graphic Designer", "Visual Designer", "Creative Designer"],
    ["UI Designer", "UX Designer", "UI/UX Designer", "Product Designer"],
    ["Web Designer", "Digital Designer", "Interactive Designer"],
    ["Art Director", "Creative Director", "Design Director"],
    ["Motion Designer", "Motion Graphics Designer", "Animator"],
    ["Video Editor", "Multimedia Specialist", "Production Artist"],
    ["Illustrator", "Digital Illustrator", "Concept Artist"],

    # Operations & HR
    ["HR Manager", "Human Resources Manager", "HR Generalist", "HR Specialist"],
    ["Recruiter", "Talent Acquisition Specialist", "Technical Recruiter",
     "Recruiting Coordinator"],
    ["Operations Manager", "Operations Director", "Director of Operations"],
    ["Supply Chain Manager", "Logistics Manager", "Supply Chain Analyst"],
    ["Procurement Manager", "Purchasing Manager", "Buyer"],
    ["Office Manager", "Administrative Manager", "Executive Assistant"],
    ["Project Manager", "Program Manager", "Project Coordinator"],
    ["Business Analyst", "Operations Analyst", "Process Analyst"],

    # Legal
    ["Attorney", "Lawyer", "Associate Attorney", "Counsel"],
    ["Paralegal", "Legal Assistant", "Legal Secretary"],
    ["Legal Counsel", "Corporate Counsel", "General Counsel"],
    ["Compliance Officer", "Compliance Manager", "Regulatory Affairs Specialist"],
    ["Contract Manager", "Contract Administrator", "Legal Analyst"],

    # Education & Research
    ["Teacher", "Educator", "Instructor", "Faculty"],
    ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"],
    ["Research Scientist", "Researcher", "Research Associate", "Research Analyst"],
    ["Teaching Assistant", "Graduate Assistant", "TA"],
    ["Principal", "School Administrator", "Dean", "Academic Advisor"],
    ["Postdoctoral Researcher", "Postdoc", "Research Fellow"],

    # Trades & Engineering
    ["Mechanical Engineer", "Mechanical Design Engineer", "Manufacturing Engineer"],
    ["Electrical Engineer", "Electronics Engineer", "Power Systems Engineer"],
    ["Civil Engineer", "Structural Engineer", "Construction Engineer"],
    ["Project Engineer", "Field Engineer", "Design Engineer"],
    ["Maintenance Technician", "Maintenance Engineer", "Facilities Technician"],
    ["Quality Inspector", "Quality Assurance Inspector", "QC Inspector"],
    ["Electrician", "Journeyman Electrician", "Master Electrician"],
    ["Plumber", "HVAC Technician", "Welder", "Fabricator"],
    ["Site Supervisor", "Construction Supervisor", "Foreman", "Superintendent"],
    ["CNC Operator", "Machine Operator", "Production Operator"],
]

LEADERSHIP_WORDS = [
    "led", "managed", "mentored", "supervised", "directed", "spearheaded",
    "headed", "oversaw", "coordinated", "championed", "facilitated",
    "trained", "coached", "delegated", "established", "built a team",
]

CERTIFICATION_KEYWORDS = [
    "certified", "certification", "certificate", "licensed", "license",
    "credential", "accredited", "registered", "board certified",
]
