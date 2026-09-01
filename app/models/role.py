from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    future_profile: Mapped[str | None] = mapped_column(Text, nullable=True)
    creation_source: Mapped[str] = mapped_column(String(50), nullable=False, default="researched_seed")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    processes: Mapped[list["Process"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    role_skills: Mapped[list["RoleSkill"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    future_responsibilities: Mapped[list["FutureResponsibility"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )
