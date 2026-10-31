
from datetime import date, datetime

from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Shift(Base):
    """Represents a scheduled manufacturing shift."""

    __tablename__ = "shifts"

    shift_id: Mapped[str] = mapped_column(
        String(50), primary_key=True
    )

    shift_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    shift_code: Mapped[str] = mapped_column(
        String(10), nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
