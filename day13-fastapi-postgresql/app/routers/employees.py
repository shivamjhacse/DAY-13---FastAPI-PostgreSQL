from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee_service import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    update_employee,
)


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee",
    description="Create a new employee and store the data in PostgreSQL.",
)
def create_employee_endpoint(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return create_employee(
        db=db,
        employee_data=employee_data,
    )


@router.get(
    "",
    response_model=list[EmployeeResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Employees",
    description="Get all employees with optional department filtering and name search.",
)
def get_employees_endpoint(
    department: Optional[str] = Query(
        default=None,
        min_length=2,
        max_length=100,
        description="Filter employees by department",
    ),
    search: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=100,
        description="Search employees by name",
    ),
    db: Session = Depends(get_db),
):
    return get_all_employees(
        db=db,
        department=department,
        search=search,
    )


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Employee",
    description="Get a single employee using employee ID.",
)
def get_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_employee(
        db=db,
        employee_id=employee_id,
    )


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Employee",
    description="Update employee information.",
)
def update_employee_endpoint(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    return update_employee(
        db=db,
        employee_id=employee_id,
        employee_data=employee_data,
    )


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse,
    status_code=status.HTTP_200_OK,
    summary="Partially Update Employee",
    description="Update only the fields provided by the client.",
)
def patch_employee_endpoint(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    return update_employee(
        db=db,
        employee_id=employee_id,
        employee_data=employee_data,
    )


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Employee",
    description="Delete an employee from PostgreSQL.",
)
def delete_employee_endpoint(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return delete_employee(
        db=db,
        employee_id=employee_id,
    )