
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProductionLine(Base):
    """
    Represents a production line within a manufacturing plant.
    """

    __tablename__ = "production_lines"

    # Primary key
    line_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    line_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Foreign key referencing the plants table
    plant_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("plants.plant_id"),
        nullable=False
    )

    # Relationship with the Plant model
    plant: Mapped["Plant"] = relationship(
        back_populates="lines"
    )

    # One production line can contain multiple machines
    machines: Mapped[list["Machine"]] = relationship(
        back_populates="production_line"
    )
