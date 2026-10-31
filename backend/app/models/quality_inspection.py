
from datetime import datetime

from sqlalchemy import (
    String, Integer, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class QualityInspection(Base):
    """Stores manufacturing quality inspection records."""

    __tablename__ = "quality_inspections"

    quality_inspection_id: Mapped[str] = mapped_column(
        String(50), primary_key=True
    )

    record_timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )

    machine_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("machines.machine_id"),
        nullable=False
    )

    line_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("production_lines.line_id"),
        nullable=False
    )

    product_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("products.product_id"),
        nullable=False
    )

    shift_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("shifts.shift_id"),
        nullable=False
    )

    inspected_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    good_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    reject_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    inspection_fail_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    source_system: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    source_record_id: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
