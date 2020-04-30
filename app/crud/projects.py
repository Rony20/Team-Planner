import pymongo

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from typing import List, Dict

from ..db.mongodb_utils import DatabaseConnector, Collections
from ..models.projects import (
    Project,
    ProjectUpdationByPmo,
    ProjectUpdationByPm,
    AllocationForProject
)

db_connector = DatabaseConnector()


def create_project(project: Project) -> bool:
    """
    create_project method takes project object as an argument and creates a record in the database.

    :param project: An object having data members such as id, name, assignedPM,... etc
    :type project: Object, required
    :return: Returns a boolean value indicating whether the project has been added to database or not.
    :rtype: bool
    """

    project = dict(project)
    if project["allocated_employees"] != None:
        project["allocated_employees"] = jsonable_encoder(
            project["allocated_employees"])
    created_document = db_connector.collection(
        Collections.PROJECTS).insert_one(project)
    return created_document.acknowledged


def get_all_project_details() -> list:
    """
    get_all_project_details method returns all projects data present inside the database.

    :return: Returns a list of project objects.
    :rtype: List
    """

    list_project = db_connector.collection(Collections.PROJECTS).find(
        {}, {"_id": 0}).sort("project_name", pymongo.ASCENDING)
    list_projects_to_be_send = []
    for project in list_project:
        list_projects_to_be_send.append(project)
    return list_projects_to_be_send


def get_project_by_pid(pid: str) -> dict:
    """
    get_project_by_pid method returns a particular project whose id is specified in the arguments.

    :param pid: An string value representing unique project in the database.
    :type pid: str
    :raises HTTPException: If no project is found of the id passed, then Error-404 is returned. 
    :return: Returns project object whose id was passed as argument, if no project is found then it raises an Exception.
    :rtype: dict
    """

    project_with_given_pid = db_connector.collection(Collections.PROJECTS).find_one(
        {"project_id": pid}, {"_id": 0})
    if project_with_given_pid == None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_with_given_pid


def get_project_by_name(project_name: str) -> list:
    """
    get_project_by_name returns a list of projects whose name is specified in the arguments.

    :param project_name: A string value represeting name of the project in the database.
    :type project_name: str
    :raises HTTPException: If no project is found of the name passed, then Error-404 is returned. 
    :return: Returns project object whose name was passed as argument, if no project is found then it raises an Exception.
    :rtype: list
    """

    list_project = []
    cursor_obj = db_connector.collection(Collections.PROJECTS).find(
        {"project_name": project_name}, {"_id": 0})
    for project in cursor_obj:
        list_project.append(project)
    if len(list_project) == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    else:
        return list_project


def update_project_details_pmo(update_details_obj: ProjectUpdationByPmo, pid: str) -> dict:
    """
    update_project_details_pmo method takes updation required in the project as object in argument and returns int.

    :param update_details_obj: An object having data members such as id, name, assignedPM,... etc
    :type update_details_obj: ProjectUpdationByPmo
    :param pid: An string value representing unique project in the database.
    :type pid: str
    :raises HTTPException: If no project is found of the name passed, then Error-404 is returned.
    :return: Returns a updated document from database otherwise returns None.
    :rtype: dict
    """

    project_at_pid = db_connector.collection(Collections.PROJECTS).find_one({
        "project_id": pid}, {"_id": 0})
    if project_at_pid == None:
        raise HTTPException(404, "Project not found")

    my_query = {"project_id": pid}
    update_details_obj = update_details_obj.dict(exclude_unset=True)
    update_details_obj = jsonable_encoder(update_details_obj)

    updated_obj = db_connector.collection(Collections.PROJECTS).find_one_and_update(
        my_query,
        {
            "$set": update_details_obj
        },
        projection={"_id": False,
                    "allocated_employees": False,
                    "description": False,
                    "status": False
                    },
        return_document=ReturnDocument.AFTER
    )
    return updated_obj


def update_project_details_pm(update_details_obj: ProjectUpdationByPm, pid: str) -> dict:
    """
    update_project_details_pm method takes updation required in the project as object in argument and returns int.

    :param update_details_obj: An object having data members such as id, name, assignedPM,... etc
    :type update_details_obj: ProjectUpdationByPm
    :param pid: An string value representing unique project in the database.
    :type pid: str
    :raises HTTPException: If no project is found of the name passed, then Error-404 is returned.
    :return: Returns a updated document from database otherwise returns None.
    :rtype: int
    """

    project_at_pid = db_connector.collection(Collections.PROJECTS).find_one({
        "project_id": pid}, {"_id": 0})

    if project_at_pid == None:
        raise HTTPException(404, "Project not found")

    update_details_obj = update_details_obj.dict(exclude_unset=True)
    update_details_obj = jsonable_encoder(update_details_obj)
    update_information_object = db_connector.collection(Collections.PROJECTS).find_one_and_update(
        {"project_id": pid},
        {
            "$set": update_details_obj
        },
        projection={"_id": False},
        return_document=ReturnDocument.AFTER
    )
    return update_information_object


def create_update_team(req_obj: Dict, pid: str) -> dict:
    """
    create_update_team method creates team of employees for a particular project 

    :param req_obj: contains list of integers representing employees
    :type req_obj: Dict
    :param pid: An string value representing unique project in the database.
    :type pid: str
    :return: Returns a updated document from database otherwise returns None.
    :rtype: dict
    """

    allocated_employees = req_obj["allocated_employees"]
    my_query = {"project_id": pid}
    for employee in allocated_employees:
        add_employee = {
            "id": employee,
            "status": "Active",
            "allocations": []
        }
        emp_object = {
            "allocated_employees": add_employee
        }
        updated_obj = db_connector.collection(Collections.PROJECTS).find_one_and_update(
            my_query,
            {
                "$push": emp_object
            },
            projection={"_id": False,
                        "project_name": False,
                        "assigned_pm": False,
                        "start_date": False,
                        "end_date": False,
                        "status": False,
                        "skillset": False,
                        "description": False},
            return_document=ReturnDocument.AFTER
        )
    return updated_obj
