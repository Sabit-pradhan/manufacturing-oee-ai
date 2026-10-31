
from sqlalchemy import String, Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database.base import Base


class Machine(Base):
    """
    Represents a machine installed on a production line.
    """

    __tablename__ = "machines"

    machine_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    machine_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    line_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("production_lines.line_id"),
        nullable=False
    )

    machine_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    nominal_rate_per_min: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    commissioned_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    # Relationship with production line
    production_line: Mapped["ProductionLine"] = relationship(
        back_populates="machines"
    )
