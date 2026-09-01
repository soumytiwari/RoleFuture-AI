# RoleFuture AI — Analysis Methodology

## Purpose

RoleFuture AI assesses how artificial intelligence may affect business roles by analysing their processes and activities.

The system does not predict that a complete job will disappear. It estimates which activities may be automated, augmented, or remain primarily human-led.

## Analysis hierarchy

```text
Role
↓
Processes
↓
Activities
↓
Current skills
↓
Assessment factors
↓
AI exposure
↓
Activities automated / augmented
↓
New responsibilities
↓
Future skills
↓
Future role profile
```

## Assessment factors

Every activity is assessed from 1 to 5 across:

- Repetitiveness
- Digital data availability
- Rule-based potential
- Language or document intensity
- Human judgment requirement
- Physical dependency
- Sensitivity and stakeholder complexity

Higher values increase exposure for the first four dimensions. Human judgment, physical dependency, and sensitivity/complexity are reversed when calculating direct exposure because higher values make full automation less likely.

## Exposure score

Each factor is normalised to 0–100:

```text
Normalised = ((factor - 1) / 4) × 100
```

The exposure score is the average of:

```text
Repetitiveness
Digital data availability
Rule-based potential
Language intensity
Reversed human judgment
Reversed physical dependency
Reversed sensitivity/complexity
```

Categories:

| Score | Category |
|---:|---|
| 0–24.99 | Low |
| 25–49.99 | Moderate |
| 50–74.99 | High |
| 75–100 | Very High |

## Automation potential

```text
30% Repetitiveness
25% Digital data availability
25% Rule-based potential
20% Language intensity
```

## Augmentation potential

```text
25% Language intensity
35% Human judgment requirement
20% Digital data availability
20% Rule-based potential
```

## Impact classification

The engine applies the same rules to every activity:

1. Exposure below 30 → `Primarily Human-Led`.
2. Automation at least 10 points above augmentation → `Automated`.
3. Augmentation equal to or above automation → `Augmented`.
4. Otherwise → `Primarily Human-Led`.

These classifications are analytical indicators, not predictions of job loss.

## Role-level change score

Role ranking combines the underlying activity results:

```text
Role Change Score =
    0.50 × Average Exposure
  + 0.30 × Average Automation
  + 0.20 × High Exposure Ratio × 100
```

This produces a comparable score for every role using the same method.

## AI explanation layer

The local language model does not calculate the numerical results. It receives structured application facts that include the role, activity scores, classifications, current/future skills, and future responsibilities.

Its output is limited to explanation and synthesis:

- Overall impact summary
- Activities AI may automate
- Activities AI may augment
- Human responsibilities
- Future skills
- Future role profile
- Transformation drivers

The response must be valid JSON. The application uses a deterministic fallback when the local model is unavailable.

## Traceability

The UI exposes the original 1–5 assessment factors, calculated scores, exposure category, impact classification, and assessment rationale. This is the project's explainability mechanism. It shows the inputs and conclusions used by the application without presenting hidden model chain-of-thought.

## Assumptions and limitations

- AI impact is assessed at activity level rather than only by job title.
- AI usually transforms tasks rather than eliminating a complete role.
- The same activity may have different outcomes in different organisations depending on data quality, controls, technology maturity, regulation, and adoption.
- The scoring model is transparent but not statistically validated as a labour-market forecast.
- The dataset represents representative corporate-service work and is not intended to describe every organisation.

## New roles and re-analysis

For a new role, the user supplies a role title and may provide a short description and department. The application first tries the local Ollama model to generate a structured role profile containing processes, activities, skills, future responsibilities, a future role profile, and 1-to-5 assessment factors. When the model is unavailable, a deterministic heuristic fallback uses the role title, supplied description, and role-family/activity keywords to construct a conservative profile and assessment factors.

The generated 1-to-5 factors are inputs to the same deterministic Python scoring engine used for the researched seed dataset. The language model never directly writes the final exposure, automation, or augmentation score.

A saved role can be re-analysed. Re-analysis regenerates the text profile, processes, activities, 1-to-5 factors, skills, future responsibilities, and numerical scores, while retaining the original role record and ID. Existing generated child records are replaced so the database does not accumulate duplicate versions of the same role.

The heuristic fallback is an algorithmic rule-based approximation, not machine learning. It checks the role/description/activity text for indicators such as data, document, routine, test, decision, stakeholder, physical, or sensitive work and maps those signals to conservative 1-to-5 factor values. It is designed for availability and reproducibility, not as a claim of objective occupational truth.
