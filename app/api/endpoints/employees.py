from fastapi import APIRouter, FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient, ReturnDocument
from typing import List, Dict
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from ...crud.employees import (
    create_employee,
    edit_employee,
    send_all_employee,
    send_employee_by_id,
    send_employee_by_name
)
from ...models.employees import (
    Employee,
    UpdateEmployee,
    PastProjects,
    CurrentProjects
)

app = FastAPI()
router = APIRouter()


@router.post("/add-employee")
def create_employee_api(employee: Employee) -> bool:
    return create_employee(employee)

# to update a particular employee details


@router.patch("/update-employee/{employee_id}")
def update_employee_api(employee_id: int, update_employee: UpdateEmployee) -> Dict:
    return edit_employee(employee_id, update_employee)


# to get all employee details

@router.get("/get-all-employees")
def send_all_employee_api() -> Dict:
    return send_all_employee()

# to get a paticular employee detail


@router.get("/get-employees/{employee_id}")
def send_employee_by_id_api(employee_id: int) -> Dict:
    return send_employee_by_id(employee_id)


# to get a particular employee with name

@router.get("/get-employee-name/{employee_name}")
def send_employee_by_name_api(employee_name: str) -> Dict:
    return send_employee_by_name(employee_name)
