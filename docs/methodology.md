# RoleFuture AI - Analysis Methodology

## Purpose

RoleFuture AI assesses how artificial intelligence may affect business roles by analysing their processes and activities.

The system does not predict that a complete job will disappear. It estimates which activities may be automated, augmented, or remain primarily human-led.

## Analysis Structure

Each role is analysed through the following hierarchy:

```text
Role
└── Processes
    └── Activities
        └── Assessment factors
            ├── AI exposure
            ├── Automation potential
            ├── Augmentation potential
            └── Impact classification

## Assessment Factors

Every activity is assessed on a scale from 1 to 5:

- Repetitiveness
- Digital data availability
- Rule-based potential
- Language or document intensity
- Human judgment requirement
- Physical dependency
- Sensitivity and stakeholder complexity

A score of 1 represents a low presence of the factor and 5 represents a high presence.

For factors that reduce AI exposure, the scoring engine reverses the value:

```text
Adjusted value = 6 - original value

This applies to:
- Human judgement requirement
- Physical dependency
- Sensitivity and complexity

## Exposure Score

The exposure score is the average of all seven normalized factors.

Each factor is converted from the 1–5 scale to a 0–100 scale:

```text
Normalized score = ((factor value - 1) / 4) × 100

The final exposure score is: 

```text
Average of:
- Repetitiveness
- Digital data availability
- Rule-based potential
- Language intensity
- Reversed human judgment
- Reversed physical dependency
- Reversed sensitivity and complexity

## Exposure Categories

| Score       | Category    |
| ------------ | ---------   |
| 0-24.99     | Low   |
| 25-49.99    | Moderate    |
| 50-74.99    | High        |
| 75-100      | Very High   |

## Automation Score

Automation potential uses the following weighted formula:

```text
30% Repetitiveness
25% Digital data availability
25% Rule-based potential
20% Language intensity

This score is higher when an activity is repetitive, digital, structured, and suitable for predictable processing.

## Augmentation Score

Augmentation potential uses the following weighted formula:

```text
25% Language intensity
35% Human judgment requirement
20% Digital data availability
20% Rule-based potential

This score represents the potential for AI to assist a person with analysis, preparation, drafting, detection, or recommendations while human judgment remains involved.

## Impact Classification

The application classifies each activity using these rules:

1. If exposure is below 30, the activity is classified as `Primarily Human-Led` .
2. If automation is at least 10 points higher than augmentation, the activity is classified as `Automated` .
3. If augmentation is equal to or higher than automation, the activity is classified as `Augmented` .
4. Otherwise, the activity is classified as `Primarily Human-Led` .

## Role-Level Analysis

Role-level metrics are calculated from the activities belonging to that role:

- Activity count
- Average exposure score
- Average automation score
- Average augmentation score
- Number of high or very-high exposure activities

The dashboard and ranking views use these stored activity-level results rather than hard-coded role outputs.

## Explainability

Each activity result includes:
- The original assessment factors
- Calculated scores
- Exposure category
- Impact classification
- Rule-based reasoning

The reasoning explains which factors influenced the result. It is an assessment rationale, not hidden model reasoning.

## Data Traceability

The application stores:
- Roles
- Processes
- Activities
- Assessment factors
- Calculated results
- Skills
- Future responsibilities
- Evidence or supporting assumptions where available

The scoring engine calculates the main results in Python. Any future language-model integration will only explain or summarize these structured results and will not control the core scores.


## Assumptions

- AI impact is assessed at activity level rather than job-title level.
- AI impact generally transforms tasks rather than eliminating complete roles.
- The scores are indicative analytical assessments, not statistically validated forecasts.
- The same activity may have different results in organizations with different technology maturity, data quality, controls, or regulations.
- Human review remains important for sensitive, complex, accountable, or stakeholder-facing work.

## Limitations

The quality of the analysis depends on the quality of the role and activity data. The current dataset represents common corporate-service activities and does not represent every organization.

The scoring model is transparent and consistent, but it is not a labour-market prediction model. It should support workforce planning and reskilling discussions rather than replace professional judgment.

EOF