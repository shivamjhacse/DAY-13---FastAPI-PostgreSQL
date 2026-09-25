from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeBase(BaseModel):
    employee_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Employee full name"
    )

    email: EmailStr

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        description="Employee phone number"
    )

    salary: Decimal = Field(
        ...,
        gt=0,
        le=9999999999,
        description="Employee salary"
    )

    joining_date: date

    department: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    designation: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    @field_validator("employee_name", "department", "designation")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        value = value.strip()

        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(value) not in range(10, 16):
            raise ValueError(
                "Phone number must contain between 10 and 15 digits"
            )

        return value

    @field_validator("joining_date")
    @classmethod
    def validate_joining_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError(
                "Joining date cannot be in the future"
            )

        return value


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    employee_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=15
    )

    salary: Decimal | None = Field(
        default=None,
        gt=0,
        le=9999999999
    )

    joining_date: date | None = None

    department: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    designation: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    @field_validator("employee_name", "department", "designation")
    @classmethod
    def validate_optional_text_fields(
        cls,
        value: str | None
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value

    @field_validator("phone")
    @classmethod
    def validate_optional_phone(
        cls,
        value: str | None
    ) -> str | None:

        if value is None:
            return value

        value = value.strip()

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits"
            )

        if len(value) not in range(10, 16):
            raise ValueError(
                "Phone number must contain between 10 and 15 digits"
            )

        return value

    @field_validator("joining_date")
    @classmethod
    def validate_optional_joining_date(
        cls,
        value: date | None
    ) -> date | None:

        if value is None:
            return value

        if value > date.today():
            raise ValueError(
                "Joining date cannot be in the future"
            )

        return value


class EmployeeResponse(EmployeeBase):
    employee_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )