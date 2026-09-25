from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models.employee import Employee
from app.routers.employees import router as employee_router



Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    description=(
        "Day 13 - FastAPI + PostgreSQL Employee Management API. "
        "Provides CRUD operations, search, department filtering, "
        "validation, error handling, and transaction management."
    ),
    version="1.0.0",
)


app.include_router(employee_router)


@app.get(
    "/",
    tags=["Health Check"],
)
def root():
    return {
        "message": "Employee Management API is running",
        "database": "PostgreSQL",
        "version": "1.0.0",
    }

#/Desktop/day13/DAY-13---FastAPI-PostgreSQL/day13-fastapi-postgresql$
#uvicorn app.main:app --reload