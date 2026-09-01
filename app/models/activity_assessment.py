from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ActivityAssessment(Base):
    __tablename__ = "activity_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"),
        nullable=False,
        unique=True,
    )

    repetitiveness: Mapped[int] = mapped_column(Integer, nullable=False)
    digital_data_availability: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    rule_based_potential: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    language_intensity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    human_judgment_requirement: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    physical_dependency: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    sensitivity_complexity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    exposure_score: Mapped[float | None] = mapped_column(Float)
    exposure_category: Mapped[str | None] = mapped_column(String(30))
    automation_score: Mapped[float | None] = mapped_column(Float)
    augmentation_score: Mapped[float | None] = mapped_column(Float)
    impact_type: Mapped[str | None] = mapped_column(String(30))
    reasoning: Mapped[str | None] = mapped_column(Text)
    assessment_source: Mapped[str] = mapped_column(String(50), nullable=False, default="researched_seed")
    analyzed_at: Mapped[datetime | None] = mapped_column(DateTime)

    activity: Mapped["Activity"] = relationship(
        back_populates="assessment",
    )
