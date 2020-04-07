from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from typing import List, Dict
from ..db.mongodb_utils import DatabaseConnector, Collections
from ..models.projects import (
    Project,
    ProjectUpdationByPmo,
    ProjectUpdationByPm,
    AllocationForProject,
)

db_connector = DatabaseConnector()


def createProject(project: Project) -> bool:
    """
    createProject method takes project object as an argument and creates a record in the database.

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


def getAllProjectDetails() -> list:
    """
    getAllProjectDetails method returns all projects data present inside the database.

    :return: Returns a list of project objects.
    :rtype: List
    """
    list_project = db_connector.collection(Collections.PROJECTS).find(
        {}, {"_id": 0}).sort("project_name", pymongo.ASCENDING)
    list_projects_to_be_send = []
    for project in list_project:
        list_projects_to_be_send.append(project)
    return list_projects_to_be_send


def getProjectByPid(pid: str) -> dict:
    """
    getProjectByPid method returns a particular project whose id is specified in the arguments.

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


def getProjectByProjectName(project_name: str) -> list:
    """
    getProjectByProjectName returns a list of projects whose name is specified in the arguments.

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


def updateProjectDetailsPmo(UpdateDetailsObj: ProjectUpdationByPmo, pid: str) -> dict:
    """
    updateProjectDetailsPmo method takes updation required in the project as object in argument and returns int.

    :param UpdateDetailsObj: An object having data members such as id, name, assignedPM,... etc
    :type UpdateDetailsObj: ProjectUpdationByPmo
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
    UpdateDetailsObj = UpdateDetailsObj.dict(exclude_unset=True)
    UpdateDetailsObj = jsonable_encoder(UpdateDetailsObj)
    if "allocated_employees" in UpdateDetailsObj:
        for employee in UpdateDetailsObj["allocated_employees"]:
            add_employee = {
                "allocated_employees": employee
            }
            updated_obj = db_connector.collection(Collections.PROJECTS).find_one_and_update(
                my_query,
                {
                    "$push": add_employee
                },
                projection={"_id": False},
                return_document=ReturnDocument.AFTER
            )
    elif "skillset" in UpdateDetailsObj:
        for skill in UpdateDetailsObj["skillset"]:
            add_skill = {
                "skillset": skill
            }
            updated_obj = db_connector.collection(
                Collections.PROJECTS).find_one_and_update(
                my_query,
                {
                    "$push": add_skill
                },
                projection={"_id": False},
                return_document=ReturnDocument.AFTER
            )
    else:
        updated_obj = db_connector.collection(Collections.PROJECTS).find_one_and_update(
            my_query,
            {
                "$set": UpdateDetailsObj
            },
            projection={"_id": False},
            return_document=ReturnDocument.AFTER
        )
    return updated_obj


def updateProjectDetailsPm(UpdateDetailsObj: ProjectUpdationByPm, pid: str) -> dict:
    """
    updateProjectDetailsPm method takes updation required in the project as object in argument and returns int.

    :param UpdateDetailsObj: An object having data members such as id, name, assignedPM,... etc
    :type UpdateDetailsObj: ProjectUpdationByPm
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

    UpdateDetailsObj = UpdateDetailsObj.dict(exclude_unset=True)
    UpdateDetailsObj = jsonable_encoder(UpdateDetailsObj)
    update_information_object = db_connector.collection(Collections.PROJECTS).find_one_and_update(
        {"project_id": pid},
        {
            "$set": UpdateDetailsObj
        },
        projection={"_id": False},
        return_document=ReturnDocument.AFTER
    )
    return update_information_object


def createUpdateTeam(req_obj: Dict, pid: str) -> dict:
    """
    createUpdateTeam method creates team of employees for a particular project 
    
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
            "employee_id": employee,
            "status": True,
            "allocation": []
        }
        emp_object = {
            "allocated_employees": add_employee
        }
        updated_obj = db_connector.collection(Collections.PROJECTS).find_one_and_update(
            my_query,
            {
                "$push": emp_object
            },
            projection={"_id": False},
            return_document=ReturnDocument.AFTER
        )
    return updated_obj
