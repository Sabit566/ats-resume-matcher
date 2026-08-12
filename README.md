# Scanline — ATS Resume Matcher

A full-stack ATS resume matcher built with FastAPI and a vanilla frontend.
The app scores resumes against a job description using semantic similarity,
skill matching, experience, education, and keyword coverage.

## What it does

- Accepts a resume file (`.pdf`, `.docx`, or `.txt`) or pasted resume text
- Accepts a pasted job description
- Computes five scoring dimensions:
  - Semantic similarity
  - Skills match
  - Experience match
  - Education match
  - Keyword coverage
- Combines the dimensions into an overall score
- Displays chart-based visual results and suggested improvements

## Architecture

```
ats-resume-matcher/
├── backend/
│   ├── main.py                # FastAPI app with /api/match and /api/health
│   ├── resume_parser.py       # Resume text extraction and metadata parsing
│   ├── jd_parser.py           # Job description section parsing
│   ├── skill_matcher.py       # Skill extraction and coverage scoring
│   ├── skills_data.py         # Skill taxonomy and synonym lookup
│   ├── semantic_matcher.py    # Semantic similarity fallback / embeddings support
│   ├── experience_matcher.py  # Experience/year/title matching and leadership detection
│   ├── education_matcher.py   # Degree-level matching
│   ├── keyword_matcher.py     # TF-IDF keyword extraction and coverage scoring
│   ├── score_engine.py        # Weighted overall score calculation
│   └── report_generator.py    # Output report with strengths and suggestions
└── frontend/
    ├── index.html             # App shell, forms, canvas elements, and Chart.js loading
    ├── style.css              # UI styles
    ├── chartManager.js        # Safe Chart.js helper and chart lifecycle handling
    └── script.js              # UI glue, API integration, rendering logic
```

## Scoring formula

- Overall =
  - 40% Semantic Similarity
  - 25% Skills Match
  - 15% Experience Match
  - 10% Education Match
  - 10% Keyword Coverage

## Dependencies

### Required

- Python 3.10+
- fastapi
- uvicorn
- python-multipart
- scikit-learn
- pdfplumber
- python-docx

### Optional

- sentence-transformers (for higher-quality semantic similarity)

## Install and run

```bash
cd backend
python -m pip install fastapi uvicorn python-multipart scikit-learn pdfplumber python-docx
python -m uvicorn main:app --reload --port 8000
```

Then open:

```text
http://localhost:8000
```

The frontend is served by FastAPI using `StaticFiles`, so no separate frontend
server is required.

## API

### `GET /api/health`

Returns:

```json
{ "status": "ok" }
```

### `POST /api/match`

Form fields:

- `jd_text` (string, required)
- `resume_file` (file, optional)
- `resume_text` (string, optional)

If `resume_file` is sent, the backend parses its contents. Otherwise, it
uses `resume_text`.

Response payload includes:

- `candidate` metadata
- `overall_score`
- `match_level`
- `breakdown` scores
- `semantic_method`
- `skills` details
- `experience`, `education`, `keyword` detail objects
- `strengths`
- `suggestions`

## Backend internals

### `main.py`

- Exposes `/api/match` and `/api/health`
- Reads resume file or pasted text
- Calls parser + matcher modules
- Combines results with `compute_overall_score`
- Builds a final report via `build_report`

### `resume_parser.py`

- Extracts text from PDF, DOCX, and plain text
- Detects email and phone patterns
- Guesses candidate name from the first non-contact heading
- Splits resume text into common sections

### `jd_parser.py`

- Extracts required/preferred qualification blocks from JD text
- Falls back to raw JD text if no marker is found

### `skill_matcher.py` / `skills_data.py`

- Uses a skill taxonomy and synonyms lookup
- Finds term matches in both resume and JD text
- Computes coverage score over JD skills
- Groups missing skills by category

### `semantic_matcher.py`

- Defaults to TF-IDF + cosine similarity
- Supports `sentence-transformers` when
  `USE_SENTENCE_TRANSFORMERS = True`
- Returns a 0–100 score and method label

### `experience_matcher.py`

- Extracts years from text using regex
- Detects title similarity using grouped title variants
- Awards leadership scoring when resume mentions key terms

### `education_matcher.py`

- Detects degree level from keywords
- Scores resumes against JD-required degree level

### `keyword_matcher.py`

- Builds JD keyword importance using TF-IDF
- Measures how many top JD keywords appear in the resume

### `score_engine.py`

- Combines the five dimension scores into a final score
- Converts the score into a match level:
  - `Excellent` 85–100
  - `Good` 70–84
  - `Moderate` 50–69
  - `Low` 0–49

### `report_generator.py`

- Builds strengths from matched skills and leadership signals
- Generates actionable improvement suggestions

## Frontend details

### `index.html`

- Loads CSS and the Chart.js library
- Uses a CDN with a fallback URL for reliability
- References `chartManager.js` before `script.js`
- Contains canvas elements for gauge, pie, and radar charts

### `chartManager.js`

- Validates that `window.Chart` is available
- Validates the target canvas element exists and has a 2D context
- Destroys any previous chart instance before creating a new one
- Exposes a reusable `createChart(canvasId, config)` helper

### `script.js`

- Manages file selection, drag/drop, and form state
- Calls the backend `/api/match` endpoint
- Separates API errors from rendering errors
- Logs detailed errors to the console
- Shows friendly user-facing messages on chart failures

## Troubleshooting

### `Chart is not defined`

- The frontend now loads Chart.js before the app script
- It also falls back to an alternate CDN if jsDelivr fails
- Chart rendering is wrapped in a safe helper that throws a clear error

### Server issues

- Make sure `uvicorn main:app --reload --port 8000` is running from the
  `backend/` folder
- Ensure required Python packages are installed
- Open `http://localhost:8000` in the browser

## Extending this project

- Add new skills and synonyms in `backend/skills_data.py`
- Add a custom JD parsing rule in `backend/jd_parser.py`
- Improve semantic scoring by enabling `sentence-transformers`
- Add more frontend charts or drill-down visualizations
- Add authentication or persistent resume history

## Optional semantic embeddings

Install the package:

```bash
python -m pip install sentence-transformers
```

Then update `backend/semantic_matcher.py`:

```python
USE_SENTENCE_TRANSFORMERS = True
```

This swaps the fallback TF-IDF similarity for a transformer-based embedding
similarity model.
