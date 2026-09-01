"""Transparent scoring engine for activity- and role-level AI impact."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.models import Activity, ActivityAssessment, Process

MIN_FACTOR = 1
MAX_FACTOR = 5


@dataclass(frozen=True)
class ActivityScore:
    exposure_score: float
    automation_score: float
    augmentation_score: float
    exposure_category: str
    impact_type: str
    reasoning: str


@dataclass(frozen=True)
class RoleAnalysis:
    role_id: int
    activity_count: int
    average_exposure: float
    average_automation: float
    average_augmentation: float
    high_exposure_count: int


def _validate_factor(value: int | float) -> float:
    numeric = float(value)
    if not MIN_FACTOR <= numeric <= MAX_FACTOR:
        raise ValueError(f"Assessment factors must be between {MIN_FACTOR} and {MAX_FACTOR}.")
    return numeric


def _to_score(value: int | float) -> float:
    """Convert a 1-to-5 factor into a 0-to-100 score."""
    numeric = _validate_factor(value)
    return ((numeric - 1) / 4) * 100


def _average(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot calculate an average from an empty list.")
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
    elif assessment.digital_data_availability <= 2:
        reasons.append("limited digital-data availability")

    if assessment.rule_based_potential >= 4:
        reasons.append("high rule-based potential")
    elif assessment.rule_based_potential <= 2:
        reasons.append("low rule-based potential")

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
            "The activity has strong potential for automated processing because "
            "it is relatively repeatable, structured, or rule-based."
        )
    elif impact_type == "Augmented":
        conclusion = (
            "AI may assist with analysis, preparation, drafting, or detection, "
            "while human judgment remains important."
        )
    else:
        conclusion = (
            "The activity is likely to remain primarily human-led, although AI "
            "may still provide supporting information."
        )

    return (
        f"The assessment shows {factor_text}. "
        f"These factors produce an exposure score of {exposure_score:.1f}/100, "
        f"an automation score of {automation_score:.1f}/100, and an "
        f"augmentation score of {augmentation_score:.1f}/100. {conclusion}"
    )


def calculate_activity_score(assessment: Any) -> ActivityScore:
    """Calculate transparent scores for one 1-to-5 activity assessment."""
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
    impact_type = classify_impact(automation_score, augmentation_score, exposure_score)

    return ActivityScore(
        exposure_score=exposure_score,
        automation_score=automation_score,
        augmentation_score=augmentation_score,
        exposure_category=exposure_category,
        impact_type=impact_type,
        reasoning=build_reasoning(
            assessment,
            exposure_score,
            automation_score,
            augmentation_score,
            impact_type,
        ),
    )


def _apply_score(assessment: ActivityAssessment, result: ActivityScore) -> None:
    assessment.exposure_score = result.exposure_score
    assessment.automation_score = result.automation_score
    assessment.augmentation_score = result.augmentation_score
    assessment.exposure_category = result.exposure_category
    assessment.impact_type = result.impact_type
    assessment.reasoning = result.reasoning
    assessment.analyzed_at = datetime.now(timezone.utc)


def analyze_and_save_assessment(db, assessment: ActivityAssessment):
    result = calculate_activity_score(assessment)
    _apply_score(assessment, result)
    db.commit()
    db.refresh(assessment)
    return assessment


def analyze_all_assessments(db):
    assessments = db.query(ActivityAssessment).all()
    for assessment in assessments:
        _apply_score(assessment, calculate_activity_score(assessment))
    db.commit()
    return assessments


def calculate_role_analysis(db, role_id: int) -> RoleAnalysis:
    """Calculate role-level metrics and persist any missing activity scores."""
    assessments = (
        db.query(ActivityAssessment)
        .join(Activity, ActivityAssessment.activity_id == Activity.id)
        .join(Process, Activity.process_id == Process.id)
        .filter(Process.role_id == role_id)
        .all()
    )

    if not assessments:
        raise ValueError(f"No assessments found for role {role_id}")

    changed = False
    for assessment in assessments:
        if (
            assessment.exposure_score is None
            or assessment.automation_score is None
            or assessment.augmentation_score is None
            or assessment.exposure_category is None
            or assessment.impact_type is None
            or assessment.reasoning is None
        ):
            _apply_score(assessment, calculate_activity_score(assessment))
            changed = True

    if changed:
        db.commit()

    exposure_scores = [a.exposure_score for a in assessments if a.exposure_score is not None]
    automation_scores = [a.automation_score for a in assessments if a.automation_score is not None]
    augmentation_scores = [a.augmentation_score for a in assessments if a.augmentation_score is not None]

    if not exposure_scores or not automation_scores or not augmentation_scores:
        raise ValueError(f"Incomplete analysis data for role {role_id}")

    high_exposure_count = sum(
        a.exposure_category in {"High", "Very High"}
        for a in assessments
    )

    return RoleAnalysis(
        role_id=role_id,
        activity_count=len(assessments),
        average_exposure=round(_average(exposure_scores), 2),
        average_automation=round(_average(automation_scores), 2),
        average_augmentation=round(_average(augmentation_scores), 2),
        high_exposure_count=high_exposure_count,
    )
