from fastapi import APIRouter
from datetime import datetime

from typing import List

from ..models.Department import Department

from ..sql.SqlDatabaseHandler import sqlDatabaseHandler as Database

router_departments = APIRouter(prefix="/api/v1/departments")

@router_departments.get(
        "/",
        response_model=List[Department]
        )
def get_departments():
    cursor = Database.getCursor()
    cursor.execute("SELECT * FROM HumanResources_Department")

    data = cursor.fetchall()

    departments = list()

    for department in data:
        departments.append(
            Department(
                DepartmentID=department[0],
                Name=department[1],
                GroupName=department[2],
                ModifiedDate=department[3]
            )
        )
    
    return departments


@router_departments.post(
    "/",
    response_model=Department
    )
def create_department(data: Department.Create):
    return Department.create(data)

@router_departments.delete(
    "/{id}",
    response_model=Department.Delete
    )
def delete_department(id: int):
    return Department.delete(id)

@router_departments.put(
    "/{id}",
    response_model=Department
    )
def update_department(id: int, department: Department.Update):
    return Department.update(id, department)