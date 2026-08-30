from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    process_id: Mapped[int] = mapped_column(
        ForeignKey("processes.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    frequency: Mapped[str] = mapped_column(String(50), nullable=False)
    human_judgment_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    process: Mapped["Process"] = relationship(back_populates="activities")
    assessment: Mapped["ActivityAssessment | None"] = relationship(
        back_populates="activity",
        uselist=False,
        cascade="all, delete-orphan",
    )
