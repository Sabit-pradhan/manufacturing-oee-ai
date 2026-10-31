
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Product(Base):
    """
    Represents a product manufactured on production lines.
    """

    __tablename__ = "products"

    # Unique product identifier
    product_id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    # Product name
    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    # Product family (A, B, C, D, etc.)
    product_family: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    # Ideal time required to manufacture one unit, in seconds
    standard_cycle_time_sec: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
