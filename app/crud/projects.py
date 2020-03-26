from fastapi import HTTPException

from ..db.mongodb_utils import DatabaseConnector, Collections
from ..models.projects import (
    Project,
    ProjectUpdationByPmo,
    ProjectUpdationByPm,
    AllocationForProject
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
    project["allocated_employees"] = dict(project["allocated_employees"])
    for key, value in project["allocated_employees"].items():
        for index in range(0, len(value)):
            (project["allocated_employees"])[key] = list(map(dict, value))
    created_document = db_connector.collection(Collections.PROJECTS).insert_one(project)
    return created_document.acknowledged


def getAllProjectDetails() -> list:
    """
    getAllProjectDetails method returns all projects data present inside the database.
    
    :return: Returns a list of project objects.
    :rtype: List
    """
    list_project = db_connector.collection(Collections.PROJECTS).find({}, {"_id": 0})
    list_projects_to_be_send = []
    for project in list_project:
        list_projects_to_be_send.append(project)
    return list_projects_to_be_send



def getProjectByPid(pid: int) -> dict:
    """
    getProjectByPid method returns a particular project whose id is specified in the arguments.
    
    :param pid: An integer value representing unique project in the database.
    :type pid: int
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
    cursor_obj = db_connector.collection(Collections.PROJECTS).find({"project_name": project_name}, {"_id": 0})
    for project in cursor_obj:
        list_project.append(project)
    if len(list_project) == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    else:
        return list_project


def updateProjectDetailsPmo(UpdateDetailsObj: ProjectUpdationByPmo, pid: int) -> int:
    """
    updateProjectDetailsPmo method takes updation required in the project as object in argument and returns int.
    
    :param UpdateDetailsObj: An object having data members such as id, name, assignedPM,... etc
    :type UpdateDetailsObj: ProjectUpdationByPmo
    :param pid: An integer value representing unique project in the database.
    :type pid: int
    :raises HTTPException: If no project is found of the name passed, then Error-404 is returned.
    :return: Returns a integer value indicating whether the project has been updated to database or not.
    :rtype: int
    """
    
    project_at_pid = db_connector.collection(Collections.PROJECTS).find_one({"project_id": pid}, {"_id": 0})
    if project_at_pid == None:
        raise HTTPException(404, "Project not found")

    UpdateDetailsObj = UpdateDetailsObj.dict(exclude_unset=True)
    UpdateDetailsObj = dict(UpdateDetailsObj)
    updated_obj = db_connector.collection(Collections.PROJECTS).update_one(
        {"project_id": pid},
        {
            "$set": UpdateDetailsObj
        }
    )
    return updated_obj.modified_count


def updateProjectDetailsPm(UpdateDetailsObj: ProjectUpdationByPm, pid: int) -> int:
    """
    updateProjectDetailsPm method takes updation required in the project as object in argument and returns int.
    
    :param UpdateDetailsObj: An object having data members such as id, name, assignedPM,... etc
    :type UpdateDetailsObj: ProjectUpdationByPm
    :param pid: An integer value representing unique project in the database.
    :type pid: int
    :raises HTTPException: If no project is found of the name passed, then Error-404 is returned.
    :return: Returns a integer value indicating whether the project has been updated to database or not.
    :rtype: int
    """
    
    project_at_pid = db_connector.collection(Collections.PROJECTS).find_one({"project_id": pid}, {"_id": 0})

    if project_at_pid == None:
        raise HTTPException(404, "Project not found")

    UpdateDetailsObj = UpdateDetailsObj.dict(exclude_unset=True)
    UpdateDetailsObj = dict(UpdateDetailsObj)
    update_information_object = db_connector.collection(Collections.PROJECTS).update_one(
        {"project_id": pid},
        {
            "$set": UpdateDetailsObj
        }
    )
    return update_information_object.modified_count
