## Step: Create the project README

**What we are doing:**  
Writing the complete `README.md` using the confirmed project structure.

**Why it matters:**  
This makes the application reproducible for judges and documents how the frontend, FastAPI backend, SQLite database, scoring engine, API, and tests work together.

**Challenge requirements completed:**  
- Setup instructions  
- Architecture documentation  
- Methodology explanation  
- API usage documentation  
- Testing instructions  
- Assumptions and limitations  

From the project root, run:

```bash
cd "/home/garun/Documents/RoleFuture AI/rolefuture-ai"

cat > README.md <<'EOF'
# RoleFuture AI

RoleFuture AI is an explainable enterprise AI application for analysing how artificial intelligence may change business roles.

It was created for the **Modus Enterprise AI Build Challenge — Assignment 6: Role-Level AI Intelligence**.

The application analyses roles through this structure:

```text
Role
↓
Processes
↓
Activities
↓
Current skills
↓
AI exposure
↓
Activities automated
↓
Activities augmented
↓
New responsibilities
↓
Future skills
↓
Future role profile
```

Users can explore individual roles, compare two roles, and identify the roles likely to experience the greatest level of AI-driven change.

## Key features

- Persistent SQLite database
- 20 representative business roles
- 58 processes and 166 activities
- Activity-level AI exposure analysis
- Automation and augmentation scores
- Exposure categories: Low, Moderate, High, and Very High
- Impact classifications:
  - Automated
  - Augmented
  - Primarily Human-Led
- Rule-based reasoning for every calculated assessment
- Role rankings
- Side-by-side role comparison
- Future responsibilities and future skills
- Browser-based frontend using Jinja2, HTML, CSS, and JavaScript
- FastAPI REST API
- Automated tests using Pytest
- No paid API key required

## Technology stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2
- HTML, CSS, and JavaScript
- Pytest
- Git

The core application does not require an external AI service. An optional local language model may be added later to improve the wording of explanations, but it must not control the numerical scores.

## Architecture

```text
Web browser
    ↓
Jinja2 templates, HTML, CSS, JavaScript
    ↓
FastAPI routes and REST API
    ↓
Application services
    ↓
Transparent Python scoring engine
    ↓
SQLAlchemy data access
    ↓
Persistent SQLite database
```

The application is divided into these layers:

- **Presentation layer:** Dashboard, role pages, and comparison interface
- **API layer:** FastAPI routes and request validation
- **Analysis layer:** Scoring, rankings, comparisons, and reasoning
- **Data layer:** SQLAlchemy models and SQLite persistence
- **Optional AI layer:** Future local-model explanation service

See the detailed architecture description in [`docs/architecture.md`](docs/architecture.md).

## Project structure

```text
rolefuture-ai/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── services/
├── data/
│   ├── seed.py
│   └── seed_additional_roles.py
├── docs/
│   ├── architecture.md
│   └── methodology.md
├── tests/
├── static/
├── templates/
├── requirements.txt
├── rolefuture.db
└── README.md
```

## Installation

From the project root, create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Database setup

The project uses the existing SQLite database file:

```text
rolefuture.db
```

The original seed script is:

```text
data/seed.py
```

It skips seeding when roles already exist.

Additional roles can be inserted safely with:

```bash
python data/seed_additional_roles.py
```

This script skips roles that are already present.

If new assessment records are added without calculated scores, recalculate them with:

```bash
python - <<'PY'
from app.database import SessionLocal
from app.services.scoring import analyze_all_assessments

db = SessionLocal()

try:
    assessments = analyze_all_assessments(db)
    print(f"Recalculated assessments: {len(assessments)}")
    print("Scores saved successfully.")
finally:
    db.close()
PY
```

## Running the application

Start the development server from the project root:

```bash
uvicorn app.main:app --reload
```

Open the application in a browser:

```text
http://127.0.0.1:8000/
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Main pages

| Page | Purpose |
|---|---|
| `/` | Dashboard with role counts, averages, high-exposure activities, and rankings |
| `/roles/1` | Role detail page for the first role |
| `/compare` | Compare two roles |
| `/docs` | Interactive Swagger API documentation |

## API endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Check whether the API is running |
| `GET /api/roles` | Retrieve all roles |
| `GET /api/roles/{role_id}` | Retrieve one role |
| `GET /api/roles/{role_id}/analysis` | Retrieve detailed role analysis |
| `GET /api/rankings` | Retrieve roles ranked by expected change |
| `GET /api/compare?role_1_id=1&role_2_id=2` | Compare two roles |

The API can be tested through the browser or the Swagger interface at `/docs`.

## Scoring methodology

Each activity is assessed using seven factors rated from 1 to 5:

- Repetitiveness
- Digital data availability
- Rule-based potential
- Language intensity
- Human judgment requirement
- Physical dependency
- Sensitivity and complexity

The scoring engine normalizes results to a 0–100 scale.

Automation potential uses:

```text
30% repetitiveness
25% digital data availability
25% rule-based potential
20% language intensity
```

Augmentation potential uses:

```text
25% language intensity
35% human judgment requirement
20% digital data availability
20% rule-based potential
```

Human judgment, physical dependency, and sensitivity/complexity are reversed when calculating direct AI exposure because higher values reduce the likelihood of direct automation.

Exposure categories are:

```text
0–24.99    Low
25–49.99   Moderate
50–74.99   High
75–100     Very High
```

Impact classification follows these rules:

- Exposure below 30: Primarily Human-Led
- Automation at least 10 points higher than augmentation: Automated
- Augmentation equal to or higher than automation: Augmented
- Otherwise: Primarily Human-Led

The numerical scores are calculated by Python in [`app/services/scoring.py`](app/services/scoring.py). They are not secretly generated by a language model.

Read the full methodology in [`docs/methodology.md`](docs/methodology.md).

## Explainability and traceability

Each assessment stores:

- The original scoring factors
- Calculated exposure score
- Exposure category
- Automation score
- Augmentation score
- Impact type
- Rule-based reasoning
- Analysis timestamp
- Supporting evidence where available

This allows users to understand how an activity-level conclusion was derived.

The application presents calculated factors and final reasoning rather than hidden model reasoning or unsupported claims.

## Rankings and comparisons

Role rankings are calculated systematically from activity-level results.

The application can compare:

- Overall role exposure
- Average automation potential
- Average augmentation potential
- Number of analysed activities
- Number of high-exposure activities
- Other role-level analysis measures

The comparison numbers are calculated by the backend from stored activity assessments.

## Testing

Run the automated test suite with:

```bash
python -m pytest -q
```

The tests cover the scoring engine and core application behavior.

Manual checks should include:

1. Open the dashboard.
2. Confirm that 20 roles are displayed.
3. Open a role detail page.
4. Confirm that activities show calculated scores.
5. Open the comparison page.
6. Compare Finance Analyst and Procurement Analyst.
7. Open the rankings.
8. Restart the application.
9. Confirm that the database records remain available.

## Assumptions

- AI exposure is assessed at activity level rather than only at job-title level.
- AI impact usually means task transformation rather than complete role replacement.
- The same activity may be automated in one organization and augmented in another.
- Scores are indicative analytical results, not guaranteed predictions.
- The dataset represents common business roles and does not describe every organization.

## Limitations

- Results depend on the quality and completeness of the activity data.
- The scoring model is a transparent analytical framework, not a statistically validated forecast.
- The application does not model every organizational factor, including technology maturity, budget, regulation, labor agreements, or employee adoption.
- Results should support workforce planning and human decision-making, not replace professional judgment.
- The initial version uses SQLite for reliable local demonstration and is not intended to be a production-scale multi-user database.

## Future enhancements

Possible future improvements include:

- Optional Ollama/local-model explanations
- Additional industries and roles
- CSV data import
- Advanced charts
- Exportable reports
- PostgreSQL support
- Administrative data management
- User authentication

These features are optional and are not required for the core MVP.

## License

See [`LICENSE`](LICENSE).