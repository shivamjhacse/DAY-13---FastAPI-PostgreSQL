from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(
    db: Session,
    employee_data: EmployeeCreate
) -> Employee:

    try:
        
        existing_email = (
            db.query(Employee)
            .filter(Employee.email == employee_data.email)
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this email already exists"
            )

        
        existing_phone = (
            db.query(Employee)
            .filter(Employee.phone == employee_data.phone)
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee with this phone number already exists"
            )

       
        employee = Employee(
            employee_name=employee_data.employee_name,
            email=str(employee_data.email),
            phone=employee_data.phone,
            salary=employee_data.salary,
            joining_date=employee_data.joining_date,
            department=employee_data.department,
            designation=employee_data.designation,
        )

        db.add(employee)

        db.commit()


        db.refresh(employee)

        return employee

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee with the provided unique information already exists"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while creating employee"
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while creating employee"
        )


def get_employee(
    db: Session,
    employee_id: int
) -> Employee:

    try:
        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )

        return employee

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while fetching employee"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while fetching employee"
        )


def get_all_employees(
    db: Session,
    department: Optional[str] = None,
    search: Optional[str] = None
) -> list[Employee]:

    try:
        query = db.query(Employee)


        if department:
            query = query.filter(
                Employee.department.ilike(department.strip())
            )

        if search:
            search_term = f"%{search.strip()}%"

            query = query.filter(
                Employee.employee_name.ilike(search_term)
            )

        return query.order_by(Employee.employee_id).all()

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while fetching employees"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while fetching employees"
        )


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
) -> Employee:

    try:
        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )

        if employee_data.email is not None:

            existing_email = (
                db.query(Employee)
                .filter(
                    Employee.email == str(employee_data.email),
                    Employee.employee_id != employee_id
                )
                .first()
            )

            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Another employee already uses this email"
                )

       
        if employee_data.phone is not None:

            existing_phone = (
                db.query(Employee)
                .filter(
                    Employee.phone == employee_data.phone,
                    Employee.employee_id != employee_id
                )
                .first()
            )

            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Another employee already uses this phone number"
                )


        update_data = employee_data.model_dump(
            exclude_unset=True
        )


        for field, value in update_data.items():

            if field == "email":
                value = str(value)

            setattr(employee, field, value)


        db.commit()


        db.refresh(employee)

        return employee

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Updated employee data violates a database constraint"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating employee"
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while updating employee"
        )


def delete_employee(
    db: Session,
    employee_id: int
) -> dict:

    try:
        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Employee with ID {employee_id} not found"
            )

        db.delete(employee)


        db.commit()

        return {
            "message": f"Employee with ID {employee_id} deleted successfully"
        }

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee cannot be deleted because it is referenced elsewhere"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while deleting employee"
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while deleting employee"
        )