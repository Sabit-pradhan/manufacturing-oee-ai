
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ProductionOrder(Base):

    __tablename__ = "production_orders"

    production_order_id: Mapped[str] = mapped_column(
        String(50), primary_key=True
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

    order_status: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    planned_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    source: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
