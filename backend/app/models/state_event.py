
from datetime import datetime

from sqlalchemy import (
    String, Integer, Float, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class StateEvent(Base):
    """Stores machine operational state events."""

    __tablename__ = "state_events"

    event_id: Mapped[str] = mapped_column(
        String(50), primary_key=True
    )

    event_timestamp: Mapped[datetime] = mapped_column(
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

    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    product_id: Mapped[str | None] = mapped_column(
        String(50),
        ForeignKey("products.product_id"),
        nullable=True
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    recorded_by: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    severity: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )

    source_event_id: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    canonical_event_id: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    duration_minutes: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
