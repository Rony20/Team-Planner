from fastapi import APIRouter, FastAPI, Query, Path, HTTPException, Depends, status
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
from ...security.auth import lead_approver_permission
from ...models.employees import (
    Employee,
    UpdateEmployee,
    PastProjects,
    CurrentProjects
)
from ...models.auth import User
from ...utils.role_manager import UserRoles

app = FastAPI()
router = APIRouter()


@router.post("/add-employee")
def create_employee_api(employee: Employee, user: User = Depends(lead_approver_permission)) -> bool:
    return create_employee(employee)

# to update a particular employee details


@router.patch("/update-employee/{employee_id}")
def update_employee_api(employee_id: int, update_employee: UpdateEmployee, user: User = Depends(lead_approver_permission)) -> Dict:
    return edit_employee(employee_id, update_employee)


# to get all employee details

@router.get("/get-all-employees")
def send_all_employee_api(user: User = Depends(lead_approver_permission)) -> Dict:
    return send_all_employee()

# to get a paticular employee detail


@router.get("/get-employees/{employee_id}")
def send_employee_by_id_api(employee_id: int, user: User = Depends(lead_approver_permission)) -> Dict:
    return send_employee_by_id(employee_id)


# to get a particular employee with name

@router.get("/get-employee-name/{employee_name}")
def send_employee_by_name_api(employee_name: str, user: User = Depends(lead_approver_permission)) -> Dict:
    return send_employee_by_name(employee_name)
