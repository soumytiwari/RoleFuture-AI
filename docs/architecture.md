# RoleFuture AI — System Architecture

## Architecture Overview

RoleFuture AI uses a layered web application architecture:

```text
┌──────────────────────────────────────┐
│              Web Browser             │
│        Jinja2, HTML, CSS, JavaScript │
└──────────────────┬───────────────────┘
                   │ HTTP requests
                   ▼
┌──────────────────────────────────────┐
│          FastAPI Application          │
│       Web pages, REST API, validation │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│          Application Services         │
│   Scoring, analysis, ranking,        │
│   comparison, and reasoning services │
└──────────────────┬───────────────────┘
                   │ SQLAlchemy
                   ▼
┌──────────────────────────────────────┐
│             SQLite Database           │
│ Roles, processes, activities, skills,│
│ assessments, scores, and evidence    │
└──────────────────────────────────────┘

Optional future component:

┌──────────────────────────────────────┐
│       Local or Free AI Model          │
│ Grounded explanations and summaries   │
└──────────────────┬───────────────────┘
                   │
                   ▼
        Structured results from services
```

## Application Layers

### Presentation Layer

The presentation layer contains:

- Dashboard
- Role detail page
- Role comparison page
- Navigation
- Activity assessment displays
- JavaScript interactions
- Charts and summary cards

Jinja2 renders the initial HTML pages. JavaScript retrieves and displays application data through FastAPI endpoints.

### API Layer

FastAPI provides:

- Health checking
- Role retrieval
- Role detail retrieval
- Role analysis
- Role rankings
- Role comparison
- Input validation
- JSON responses
- HTML page routes

Current API endpoints include:

```text
GET /api/health
GET /api/roles
GET /api/roles/{role_id}
GET /api/roles/{role_id}/analysis
GET /api/rankings
GET /api/compare?role_1_id=1&role_2_id=2
```

### Application and Analysis Layer

The analysis layer contains reusable Python services.

The scoring service:

1. Reads assessment factors.
2. Converts values from a 1–5 scale to a 0–100 scale.
3. Calculates exposure.
4. Calculates automation potential.
5. Calculates augmentation potential.
6. Assigns an exposure category.
7. Assigns an impact classification.
8. Generates assessment rationale.
9. Saves the calculated result to the database.

The role-analysis service aggregates activity results into role-level metrics.

The ranking service sorts roles using their calculated impact metrics.

The comparison service retrieves two roles and calculates their metric differences.

### Data Layer

SQLite provides persistent local storage.

SQLAlchemy is used to:

- Define database models
- Manage relationships
- Query records
- Save analysis results
- Maintain database persistence across application restarts

The main relationships are:

```text
Role
 ├── many Processes
 │    └── many Activities
 │         └── one ActivityAssessment
 ├── many RoleSkills
 │    └── one Skill
 └── many FutureResponsibilities
```

### Optional AI Explanation Layer

The core application does not depend on an external AI service.

The optional AI layer may receive structured information such as:

- Role title
- Activity name
- Assessment factors
- Calculated scores
- Impact classification
- Stored rationale
- Future responsibilities
- Future skills

It may generate:

- Plain-language activity explanations
- Future role summaries
- Comparison summaries
- Reskilling recommendations

The optional model will not calculate or replace the core scores. The transparent Python scoring engine remains the source of the numerical results.

## End-to-End User Flow

```text
1. User opens the dashboard.
2. FastAPI retrieves persistent role data.
3. The application reads saved activity assessments.
4. Role-level metrics are calculated.
5. The dashboard displays rankings and summary metrics.
6. User opens a role.
7. The application displays processes, activities, scores, and rationale.
8. User selects two roles for comparison.
9. The comparison service calculates differences.
10. The UI displays the comparison results.
```

## Technology Stack

| Layer | Technology |
|---|---|
| Programming language | Python |
| Backend framework | FastAPI |
| Templates | Jinja2 |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Testing | Pytest |
| Version control | Git |
| Optional AI | Locally runnable or free-tier model |

## Design Principles

- Scores are calculated transparently.
- Results are based on stored activity data.
- The system processes records systematically.
- The database persists data between restarts.
- The frontend is separate from scoring logic.
- The application works without an external AI provider.
- New roles can be added without changing the scoring formulas.

