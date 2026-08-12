# Scanline — ATS Resume Matcher

A full-stack ATS resume matcher built with **FastAPI** and a **vanilla JavaScript frontend**. The application evaluates resumes against job descriptions using semantic similarity, skill matching, experience, education, and keyword coverage.

## What it does

* Accepts a resume file (`.pdf`, `.docx`, or `.txt`) or pasted resume text
* Accepts a pasted job description
* Computes five scoring dimensions:

  * Semantic similarity
  * Skills match
  * Experience match
  * Education match
  * Keyword coverage
* Combines the dimensions into an overall ATS match score
* Displays chart-based visual results
* Provides strengths and suggested improvements
* Supports drag-and-drop resume upload
* Provides a FastAPI backend with REST API endpoints

## Architecture

```text
ats-resume-matcher/
├── backend/
│   ├── main.py                # FastAPI application and API endpoints
│   ├── resume_parser.py       # Resume text extraction and metadata parsing
│   ├── jd_parser.py           # Job description section parsing
│   ├── skill_matcher.py       # Skill extraction and coverage scoring
│   ├── skills_data.py         # Skill taxonomy and synonym lookup
│   ├── semantic_matcher.py    # Semantic similarity and embeddings support
│   ├── experience_matcher.py  # Experience, title, and leadership matching
│   ├── education_matcher.py   # Degree-level matching
│   ├── keyword_matcher.py     # TF-IDF keyword extraction and coverage scoring
│   ├── score_engine.py        # Weighted overall score calculation
│   └── report_generator.py    # Strengths and improvement suggestions
│
├── docs/
│   ├── index.html             # Frontend application interface
│   ├── style.css              # Frontend styling
│   ├── chartManager.js        # Chart.js management and lifecycle handling
│   └── script.js              # UI logic and API integration
│
├── .gitattributes             # GitHub Linguist language detection settings
├── .gitignore
└── README.md
```

## Technology Stack

### Backend

* Python 3.10+
* FastAPI
* Uvicorn
* Scikit-learn
* pdfplumber
* python-docx
* python-multipart

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Chart.js

### Optional

* sentence-transformers for higher-quality semantic similarity

## Scoring Formula

The overall ATS score is calculated using five weighted dimensions:

| Component           | Weight |
| ------------------- | -----: |
| Semantic Similarity |    40% |
| Skills Match        |    25% |
| Experience Match    |    15% |
| Education Match     |    10% |
| Keyword Coverage    |    10% |

### Match Levels

|  Score | Match Level |
| -----: | ----------- |
| 85–100 | Excellent   |
|  70–84 | Good        |
|  50–69 | Moderate    |
|   0–49 | Low         |

## Dependencies

### Required

```text
Python 3.10+
fastapi
uvicorn
python-multipart
scikit-learn
pdfplumber
python-docx
```

### Optional

```text
sentence-transformers
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Sabit566/ats-resume-matcher.git
cd ats-resume-matcher
```

Install the required Python packages:

```bash
python -m pip install fastapi uvicorn python-multipart scikit-learn pdfplumber python-docx
```

For optional transformer-based semantic similarity:

```bash
python -m pip install sentence-transformers
```

## Run the Application

Move into the backend directory:

```bash
cd backend
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000
```

The frontend is served by FastAPI using `StaticFiles`, so a separate frontend development server is not required.

## API

### `GET /api/health`

Checks whether the backend is running.

Example response:

```json
{
  "status": "ok"
}
```

### `POST /api/match`

Matches a resume against a job description.

#### Form Fields

| Field         | Type   | Required |
| ------------- | ------ | -------- |
| `jd_text`     | string | Yes      |
| `resume_file` | file   | No       |
| `resume_text` | string | No       |

The application accepts a resume either as an uploaded `.pdf`, `.docx`, or `.txt` file, or as pasted resume text.

#### Response

The response includes:

* Candidate metadata
* Overall ATS score
* Match level
* Score breakdown
* Semantic matching method
* Skills analysis
* Experience analysis
* Education analysis
* Keyword analysis
* Strengths
* Improvement suggestions

## Backend Internals

### `main.py`

* Provides `/api/match`
* Provides `/api/health`
* Reads uploaded resume files or pasted resume text
* Coordinates the parser and matching modules
* Calculates the final score
* Generates the final report

### `resume_parser.py`

* Extracts text from PDF, DOCX, and TXT files
* Detects email and phone patterns
* Attempts to identify the candidate name
* Splits resume content into common sections

### `jd_parser.py`

* Extracts required and preferred qualification sections
* Falls back to the complete job description when specific sections cannot be identified

### `skill_matcher.py` / `skills_data.py`

* Uses a skill taxonomy and synonym mapping
* Detects skills in resumes and job descriptions
* Calculates skill coverage
* Groups missing skills by category

### `semantic_matcher.py`

* Uses TF-IDF and cosine similarity by default
* Supports `sentence-transformers`
* Produces a semantic similarity score from 0–100
* Reports the method used for semantic matching

### `experience_matcher.py`

* Extracts years of experience using regular expressions
* Detects job-title similarity
* Recognizes grouped title variants
* Provides additional scoring for leadership indicators

### `education_matcher.py`

* Detects degree levels from resume and job description text
* Compares the candidate's education with the required degree level

### `keyword_matcher.py`

* Uses TF-IDF to identify important job-description keywords
* Measures keyword coverage in the resume

### `score_engine.py`

* Combines the five scoring dimensions
* Calculates the final ATS score
* Converts the score into a match level

### `report_generator.py`

* Generates strengths based on matching results
* Identifies useful improvement areas
* Produces actionable suggestions for the candidate

## Frontend

The frontend is located in the `docs/` directory.

### `index.html`

* Provides the main ATS Resume Matcher interface
* Loads the frontend stylesheet
* Loads Chart.js
* Loads `chartManager.js` before `script.js`
* Contains the required canvas elements for charts
* Provides resume upload and job-description input interfaces

### `style.css`

* Contains the application's visual styling
* Controls layout, forms, buttons, results, and responsive presentation

### `chartManager.js`

* Checks whether Chart.js is available
* Validates canvas elements
* Creates and manages charts
* Destroys previous chart instances before creating new ones
* Provides a reusable `createChart()` helper

### `script.js`

* Handles resume file selection
* Supports drag-and-drop interaction
* Manages form state
* Sends requests to `/api/match`
* Processes API responses
* Renders ATS results
* Handles API and chart-rendering errors
* Displays user-friendly error messages

## Charts and Results

The frontend provides visual representations of the ATS analysis, including:

* Overall ATS score
* Score breakdown
* Skills analysis
* Experience analysis
* Education analysis
* Keyword coverage
* Strengths
* Improvement suggestions

The application uses Chart.js for interactive data visualization.

## Troubleshooting

### `Chart is not defined`

If Chart.js fails to load:

* Check your internet connection
* Ensure Chart.js is loaded before `script.js`
* Check the browser console for CDN errors
* Verify that the Chart.js fallback is available

### Server Issues

Make sure the backend is running from the `backend/` directory:

```bash
python -m uvicorn main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000
```

### Resume Upload Issues

Supported formats:

```text
.pdf
.docx
.txt
```

Make sure the uploaded file is readable and that the required Python dependencies are installed.

## GitHub Language Detection

The repository uses `.gitattributes` to ensure the frontend source files inside `docs/` can be recognized by GitHub Linguist.

The frontend contains:

```text
HTML
CSS
JavaScript
```

Minified JavaScript and CSS files are configured to be treated as generated files so they do not distort the repository's language statistics.

## Extending the Project

Possible future improvements include:

* Add more skills and synonyms
* Improve job-description parsing
* Improve semantic similarity using transformer embeddings
* Add additional frontend visualizations
* Add authentication
* Add persistent resume history
* Add resume comparison between multiple candidates
* Add downloadable ATS reports
* Add job-specific resume recommendations

## Optional Semantic Embeddings

Install the package:

```bash
python -m pip install sentence-transformers
```

Then enable transformer-based semantic matching in:

```text
backend/semantic_matcher.py
```

Set:

```python
USE_SENTENCE_TRANSFORMERS = True
```

This replaces the default TF-IDF similarity approach with transformer-based embedding similarity.

## Project Repository

GitHub:

https://github.com/Sabit566/ats-resume-matcher

---

**Scanline — ATS Resume Matcher**

A full-stack resume-to-job matching application built with **FastAPI, Python, HTML, CSS, JavaScript, and Chart.js**.
