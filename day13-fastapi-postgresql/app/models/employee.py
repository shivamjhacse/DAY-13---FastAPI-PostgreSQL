from datetime import date, datetime

from sqlalchemy import Date, DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Employee(Base):
    __tablename__ = "employees"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    employee_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False
    )

    salary: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    joining_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    department: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )