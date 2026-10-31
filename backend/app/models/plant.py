
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Plant(Base):
    """
    Represents a manufacturing plant.
    """

    __tablename__ = "plants"

    # Primary key
    plant_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    plant_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    source: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    # One plant can have multiple production lines
    lines: Mapped[list["ProductionLine"]] = relationship(
        back_populates="plant"
    )
