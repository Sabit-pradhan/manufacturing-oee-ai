
from datetime import datetime

from sqlalchemy import (
    String, Integer, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProductionCount(Base):
    """Stores production count and correction records."""

    __tablename__ = "production_counts"

    production_count_id: Mapped[str] = mapped_column(
        String(50), primary_key=True
    )

    record_id: Mapped[str] = mapped_column(
        String(50), nullable=False
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

    total_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    good_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    reject_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    inspected_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    inspection_fail_count: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    record_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    count_adjustment: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    source_system: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    shift_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("shifts.shift_id"),
        nullable=False
    )

    production_order_id: Mapped[str | None] = mapped_column(
        String(50),
        ForeignKey("production_orders.production_order_id"),
        nullable=True
    )

    source_record_id: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
