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
    createProject method create project and return boolean value 
    based on wether the project is created successfully or not
    """

    project = dict(project)
    project["allocated_employees"] = dict(project["allocated_employees"])
    for key, value in project["allocated_employees"].items():
        for index in range(0, len(value)):
            (project["allocated_employees"])[key] = list(map(dict, value))
    created_document = db_connector.collection(Collections.PROJECTS).insert_one(project)
    return created_document.acknowledged


def getAllProjectDetails():
    """
    getAllProjectDetails method return all project list which is used to display project on dashboard
    """

    list_project = db_connector.collection(Collections.PROJECTS).find({}, {"_id": 0})
    list_projects_to_be_send = []
    for project in list_project:
        list_projects_to_be_send.append(project)
    return list_projects_to_be_send



def getProjectByPid(pid: int):
    """
    getProjectByPid method allow to search the project by project id
    """

    project_with_given_pid = db_connector.collection(Collections.PROJECTS).find_one(
        {"project_id": pid}, {"_id": 0})
    if project_with_given_pid == None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_with_given_pid


def getProjectByProjectName(project_name: str):
    """
    getProjectByProjectName method allow to search project by project name
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
    updateProjectDetailsPmo method allow Pmo to update project details 
    it return number of project for which details are modified (which is 0 OR 1)
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
    updateProjectDetailsPm method allows pm to update project details
    It also return integer which specify number of project modified (which is also 0 OR 1)
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
