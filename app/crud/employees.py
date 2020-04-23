from fastapi import APIRouter, FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from fastapi.encoders import jsonable_encoder
from typing import List, Dict

from ..db.mongodb_utils import DatabaseConnector, Collections
from ..models.employees import (
    Employee,
    UpdateEmployee,
    PastProjects,
    CurrentProjects,
    AllocationForProject,
    Availability
)

db_connector = DatabaseConnector()


def create_employee(employee: Employee) -> bool:
    """
    create_employee method takes employee object as argument and adds employee in the database.

    :param employee: Employee object having data members like id, name, skills, current_projects, past_projects,...etc.
    :type employee: Employee
    :return: Return a boolean value indicating whether the employee has been added to database or not.
    :rtype: bool
    """

    response_object = db_connector.collection(
        Collections.EMPLOYEES).insert_one({
            "employee_id": employee.employee_id,
            "employee_name": employee.employee_name,
            "designation": employee.designation,
            "skills": employee.skills,
            "past_projects": jsonable_encoder(employee.past_projects),
            "current_projects": jsonable_encoder(employee.current_projects),
            "availability": jsonable_encoder(employee.availability),
            "is_allocated": employee.is_allocated
        })
    return response_object.acknowledged


def edit_employee(employee_id: int, update_employee: UpdateEmployee) -> dict:
    """
    edit_employee method takes updation required in employee as object in argument and updates employee in the database.

    :param employee_id: Integer represeting a partiular employee in the database.
    :type employee_id: int
    :param update_employee: UpdateEmployee object having data members like skills, current_projects, past_projects,...etc.
    :type update_employee: UpdateEmployee
    :return: Returns a dict containing how many records have been updated in the database, message and status code.
    :rtype: Dict
    """

    my_query = {"employee_id": employee_id}
    new_values = update_employee.dict(exclude_unset=True)

    if "current_projects" or "past_projects" in new_values:
        changed_employee = db_connector.collection(
            Collections.EMPLOYEES).find_one_and_update(
            my_query,
            {
                "$push": jsonable_encoder(new_values)
            },
            projection={"_id": False},
            return_document=ReturnDocument.AFTER)
    else:
        changed_employee = db_connector.collection(
            Collections.EMPLOYEES).find_one_and_update(
            my_query,
            {
                "$set": jsonable_encoder(new_values)
            },
            projection={"_id": False},
            return_document=ReturnDocument.AFTER)
    return changed_employee


def send_all_employee() -> List:
    """
    send_all_employee method returns all employee details present in the database.

    :return: Returns a dict containing a list of employee with details, message and status code.
    :rtype: dict
    """
    all_employees = []
    for emp_obj in db_connector.collection(
            Collections.EMPLOYEES).find({}, {"_id": False}):
        all_employees.append(emp_obj)
    return all_employees



def send_employee_by_id(employee_id: int) -> dict:
    """
    send_employee_by_id method takes employee id as argument and returns that particular employee object from the database.

    :param employee_id: Integer representing a particular employee in the database.
    :type employee_id: int
    :raises HTTPException: If no employee is found whose id matches with the passed argument, then it raises Error-404 Exception.
    :return: Returns a dict containing an object of employee with details, message and status code.
    :rtype: dict
    """
    my_query = {"employee_id": employee_id}
    emp_obj = db_connector.collection(
        Collections.EMPLOYEES).find_one(my_query, {"_id": False})
    if(emp_obj is None):
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "employee": emp_obj,
    }


def send_employee_by_name(employee_name: str) -> dict:
    """
    send_employee_by_name method takes employee name as argument and returns that particular employee object from the database.

    :param employee_name: String representing a particular employee in the database.
    :type employee_name: str
    :raises HTTPException: If no employee is found whose id matches with the passed argument, then it raises Error-404 Exception.
    :return: Returns a an object of employee with details.
    :rtype: dict
    """
    my_query = {"employee_name": employee_name}
    for emp_obj in db_connector.collection(
            Collections.EMPLOYEES).find(my_query, {"_id": False}):
        return emp_obj
    raise HTTPException(status_code=404, detail="Employee not Found")
