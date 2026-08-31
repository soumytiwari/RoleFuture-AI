# RoleFuture AI

RoleFuture AI is an explainable enterprise AI application for analysing how artificial intelligence may change business roles.

It implements the challenge flow:

```text
Role
↓
Processes
↓
Activities
↓
Current Skills
↓
AI Exposure
↓
Activities Automated
↓
Activities Augmented
↓
New Responsibilities
↓
Future Skills
↓
Future Role Profile
```

Users can inspect individual roles, compare two roles, and rank roles by expected AI-driven change.

## What makes it an AI application?

The application uses a **hybrid, explainable architecture**:

1. Persistent structured role/activity data is stored in SQLite.
2. A transparent Python scoring engine calculates exposure, automation, augmentation, and impact classification.
3. A local Ollama-compatible language model can turn those structured results into readable workforce-analysis explanations.
4. The AI model does not control the numerical scores or invent the underlying data.
5. A deterministic fallback keeps the application working when Ollama is unavailable.

## Technology

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2
- HTML / CSS / JavaScript
- Pytest
- Optional Ollama local model

No paid API key is required for the core application.

## Project structure

```text
rolefuture-ai/
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── services/
├── data/
│   ├── seed.py
│   ├── seed_additional_roles.py
│   └── seed_all.py
├── docs/
│   ├── architecture.md
│   └── methodology.md
├── templates/
├── tests/
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Create the dataset

Run the single repeatable seed command:

```bash
python -m data.seed_all
```

This creates the database tables, seeds the two original roles plus the additional representative roles, adds current and future skills, creates role-specific processes and activities, and calculates/saves all activity scores.

The resulting database is persistent in:

```text
rolefuture.db
```

## Start the application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

Interactive Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## Ollama AI mode

The application works without Ollama. To enable richer explanations, install Ollama separately and make sure the configured model is available.

Default settings:

```text
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_TIMEOUT=45
```

Environment variables can override these values.

Example:

```bash
export OLLAMA_MODEL=llama3.2:3b
```

The AI status can be checked from:

```text
GET /api/ai/status
```

When the local model is unavailable, the role and comparison pages clearly label the result as a deterministic fallback.

## Main pages

| Page | Purpose |
|---|---|
| `/` | Dashboard, role ranking, aggregate metrics |
| `/roles/{id}` | Full role analysis, scoring factors, AI workforce analysis |
| `/compare` | Compare two roles and generate an AI comparison explanation |
| `/docs` | Swagger API documentation |

## API endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Application health |
| `GET /api/ai/status` | Local model availability |
| `GET /api/roles` | List roles |
| `GET /api/roles/{role_id}` | Detailed role data |
| `GET /api/roles/{role_id}/analysis` | Role-level metrics |
| `GET /api/roles/{role_id}/explanation` | Grounded AI/fallback workforce analysis |
| `GET /api/rankings` | Rank roles by change score |
| `GET /api/compare?role_1_id=1&role_2_id=2` | Compare two roles numerically |
| `GET /api/compare/explanation?role_1_id=1&role_2_id=2` | Explain the comparison with local AI/fallback |

## Scoring methodology

Each activity has seven assessment factors scored 1–5. Exposure is calculated from normalised factors, while automation and augmentation use transparent weighted formulas.

The role-change ranking is:

```text
0.50 × Average Exposure
+ 0.30 × Average Automation
+ 0.20 × High Exposure Ratio × 100
```

The complete methodology is documented in [`docs/methodology.md`](docs/methodology.md).

## Explainability

For each activity the UI exposes:

- Original 1–5 factors
- Exposure score
- Automation score
- Augmentation score
- Exposure category
- Impact classification
- Assessment rationale

For each role the AI layer can additionally explain:

- Overall impact
- Activities that may be automated
- Activities that may be augmented
- Human responsibilities
- Future skills
- Future role profile
- Main transformation drivers

The project calls these **assessment rationale / calculation details**, not hidden model chain-of-thought.

## Testing

Run:

```bash
python -m pytest -q
```

The test suite covers scoring boundaries, factor validation, impact classification, role-level aggregation, and the local-AI fallback behaviour.

For the final demo also verify:

```text
1. Dashboard loads.
2. Roles are persistent after restart.
3. Role detail loads activities and score factors.
4. AI analysis displays either local AI or the fallback.
5. Finance Analyst and Procurement Analyst comparison works.
6. Ranking page/API returns ordered results.
7. Swagger documentation is available.
```

## Assumptions and limitations

The score is an indicative analytical framework, not a statistically validated labour-market prediction. AI impact varies by organisation, data quality, controls, technology maturity, regulation, and adoption. The model should support workforce planning and reskilling decisions rather than replace human judgment.
