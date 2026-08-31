from types import SimpleNamespace

from app.services.scoring import (
    calculate_activity_score,
    classify_exposure,
)


def make_assessment(**overrides):
    values = {
        "repetitiveness": 5,
        "digital_data_availability": 5,
        "rule_based_potential": 4,
        "language_intensity": 4,
        "human_judgment_requirement": 3,
        "physical_dependency": 1,
        "sensitivity_complexity": 3,
    }

    values.update(overrides)
    return SimpleNamespace(**values)


def test_highly_structured_activity_has_high_exposure():
    assessment = make_assessment()

    result = calculate_activity_score(assessment)

    assert 0 <= result.exposure_score <= 100
    assert 0 <= result.automation_score <= 100
    assert 0 <= result.augmentation_score <= 100
    assert result.exposure_category in {
        "Low",
        "Moderate",
        "High",
        "Very High",
    }
    assert result.impact_type in {
        "Automated",
        "Augmented",
        "Primarily Human-Led",
    }
    assert result.reasoning


def test_high_human_judgment_reduces_exposure():
    low_judgment = make_assessment(human_judgment_requirement=1)
    high_judgment = make_assessment(human_judgment_requirement=5)

    low_judgment_result = calculate_activity_score(low_judgment)
    high_judgment_result = calculate_activity_score(high_judgment)

    assert high_judgment_result.exposure_score < low_judgment_result.exposure_score


def test_exposure_categories():
    assert classify_exposure(20) == "Low"
    assert classify_exposure(25) == "Moderate"
    assert classify_exposure(50) == "High"
    assert classify_exposure(75) == "Very High"
