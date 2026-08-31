# app/services/scoring.py

from dataclasses import dataclass
from typing import Any

from datetime import datetime, timezone

from app.models import ActivityAssessment, Activity, Process


# Activity score is a structured representation of the calculated scores and classifications for an activity assessment.
@dataclass
class ActivityScore:
    exposure_score: float
    automation_score: float
    augmentation_score: float
    exposure_category: str
    impact_type: str
    reasoning: str


def _to_score(value: int | float) -> float:
    """Convert a 1-to-5 factor into a 0-to-100 score."""
    return ((float(value) - 1) / 4) * 100


def _average(values: list[float]) -> float:
    return sum(values) / len(values)


def classify_exposure(score: float) -> str:
    if score < 25:
        return "Low"
    if score < 50:
        return "Moderate"
    if score < 75:
        return "High"
    return "Very High"


def classify_impact(
    automation_score: float,
    augmentation_score: float,
    exposure_score: float,
) -> str:
    """
    Classify the likely type of AI impact.

    Automation wins when automation potential is substantially higher.
    Augmentation wins when human judgment and AI assistance are both important.
    Otherwise, the activity remains primarily human-led.
    """
    if exposure_score < 30:
        return "Primarily Human-Led"

    if automation_score >= augmentation_score + 10:
        return "Automated"

    if augmentation_score >= automation_score:
        return "Augmented"

    return "Primarily Human-Led"


def build_reasoning(
    assessment: Any,
    exposure_score: float,
    automation_score: float,
    augmentation_score: float,
    impact_type: str,
) -> str:
    reasons = []

    if assessment.repetitiveness >= 4:
        reasons.append("high repetitiveness")
    elif assessment.repetitiveness <= 2:
        reasons.append("low repetitiveness")

    if assessment.digital_data_availability >= 4:
        reasons.append("strong digital-data availability")

    if assessment.rule_based_potential >= 4:
        reasons.append("high rule-based potential")

    if assessment.language_intensity >= 4:
        reasons.append("substantial language or document content")

    if assessment.human_judgment_requirement >= 4:
        reasons.append("high human judgment requirements")

    if assessment.physical_dependency >= 4:
        reasons.append("significant physical-world dependency")

    if assessment.sensitivity_complexity >= 4:
        reasons.append("high sensitivity or stakeholder complexity")

    if not reasons:
        reasons.append("mixed characteristics across the assessment factors")

    factor_text = ", ".join(reasons)

    if impact_type == "Automated":
        conclusion = (
            "The activity has strong potential for automated processing "
            "because it is relatively repeatable, structured, or rule-based."
        )
    elif impact_type == "Augmented":
        conclusion = (
            "AI may assist with analysis, preparation, drafting, or detection, "
            "while human judgment remains important."
        )
    else:
        conclusion = (
            "The activity is likely to remain primarily human-led, although "
            "AI may still provide supporting information."
        )

    return (
        f"The assessment shows {factor_text}. "
        f"These factors produce an exposure score of {exposure_score:.1f}/100, "
        f"an automation score of {automation_score:.1f}/100, and an "
        f"augmentation score of {augmentation_score:.1f}/100. "
        f"{conclusion}"
    )


def calculate_activity_score(assessment: Any) -> ActivityScore:
    """
    Calculate transparent scores for one ActivityAssessment.

    All input factors are expected to use a 1-to-5 scale.
    """

    # AI exposure considers all seven factors.
    # Human judgment, physical dependency, and complexity reduce exposure.
    exposure_score = _average(
        [
            _to_score(assessment.repetitiveness),
            _to_score(assessment.digital_data_availability),
            _to_score(assessment.rule_based_potential),
            _to_score(assessment.language_intensity),
            _to_score(6 - assessment.human_judgment_requirement),
            _to_score(6 - assessment.physical_dependency),
            _to_score(6 - assessment.sensitivity_complexity),
        ]
    )

    automation_score = (
        _to_score(assessment.repetitiveness) * 0.30
        + _to_score(assessment.digital_data_availability) * 0.25
        + _to_score(assessment.rule_based_potential) * 0.25
        + _to_score(assessment.language_intensity) * 0.20
    )

    augmentation_score = (
        _to_score(assessment.language_intensity) * 0.25
        + _to_score(assessment.human_judgment_requirement) * 0.35
        + _to_score(assessment.digital_data_availability) * 0.20
        + _to_score(assessment.rule_based_potential) * 0.20
    )

    exposure_score = round(exposure_score, 2)
    automation_score = round(automation_score, 2)
    augmentation_score = round(augmentation_score, 2)

    exposure_category = classify_exposure(exposure_score)
    impact_type = classify_impact(
        automation_score,
        augmentation_score,
        exposure_score,
    )

    reasoning = build_reasoning(
        assessment=assessment,
        exposure_score=exposure_score,
        automation_score=automation_score,
        augmentation_score=augmentation_score,
        impact_type=impact_type,
    )

    return ActivityScore(
        exposure_score=exposure_score,
        automation_score=automation_score,
        augmentation_score=augmentation_score,
        exposure_category=exposure_category,
        impact_type=impact_type,
        reasoning=reasoning,
    )

# here we saving the assessment to the database after calculating the score

def analyze_and_save_assessment(db, assessment):
    """Calculate an assessment and save the results to SQLite."""

    result = calculate_activity_score(assessment)

    assessment.exposure_score = result.exposure_score
    assessment.automation_score = result.automation_score
    assessment.augmentation_score = result.augmentation_score
    assessment.exposure_category = result.exposure_category
    assessment.impact_type = result.impact_type
    assessment.reasoning = result.reasoning
    assessment.analyzed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(assessment)

    return assessment


def analyze_all_assessments(db):
    """Calculate and save every activity assessment."""

    assessments = db.query(ActivityAssessment).all()

    for assessment in assessments:
        result = calculate_activity_score(assessment)

        assessment.exposure_score = result.exposure_score
        assessment.automation_score = result.automation_score
        assessment.augmentation_score = result.augmentation_score
        assessment.exposure_category = result.exposure_category
        assessment.impact_type = result.impact_type
        assessment.reasoning = result.reasoning
        assessment.analyzed_at = datetime.now(timezone.utc)

    db.commit()

    return assessments

# Role Analysis is a structured representation of the aggregated scores and classifications for all activities in a role.
@dataclass
class RoleAnalysis:
    role_id: int
    activity_count: int
    average_exposure: float
    average_automation: float
    average_augmentation: float
    high_exposure_count: int

# This function does not change the database. It reads the saved activity scores and creates a role summary.
def calculate_role_analysis(db, role_id: int) -> RoleAnalysis:
    """Calculate summary scores for one role."""

    assessments = (
        db.query(ActivityAssessment)
        .join(Activity, ActivityAssessment.activity_id == Activity.id)
        .join(Process, Activity.process_id == Process.id)
        .filter(Process.role_id == role_id)
        .all()
    )

    if not assessments:
        raise ValueError(f"No assessments found for role {role_id}")

    exposure_scores = [
        assessment.exposure_score
        for assessment in assessments
        if assessment.exposure_score is not None
    ]

    automation_scores = [
        assessment.automation_score
        for assessment in assessments
        if assessment.automation_score is not None
    ]

    augmentation_scores = [
        assessment.augmentation_score
        for assessment in assessments
        if assessment.augmentation_score is not None
    ]

    high_exposure_count = sum(
        assessment.exposure_category in {"High", "Very High"}
        for assessment in assessments
    )

    return RoleAnalysis(
        role_id=role_id,
        activity_count=len(assessments),
        average_exposure=round(sum(exposure_scores) / len(exposure_scores), 2),
        average_automation=round(
            sum(automation_scores) / len(automation_scores), 2
        ),
        average_augmentation=round(
            sum(augmentation_scores) / len(augmentation_scores), 2
        ),
        high_exposure_count=high_exposure_count,
    )
