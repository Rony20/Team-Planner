from fastapi import APIRouter
from typing import List, Dict

from ...crud.projects import (
    updateProjectDetailsPmo,
    updateProjectDetailsPm,
    getProjectByProjectName,
    getProjectByPid,
    createProject,
    getAllProjectDetails,
    createUpdateTeam
)

from ...models.projects import (
    ProjectUpdationByPmo,
    ProjectUpdationByPm,
    Project,
    AllocationForProject,
)

router = APIRouter()

"""
    api which create new project
"""
@router.post("/api/create-project/")
def createProjectApi(project: Project) -> bool:
    return createProject(project)


"""
    api which will get all projects information
"""
@router.get("/api/all-project-details")
def getAllProjectDetailsApi():
    return getAllProjectDetails()


"""
    api which will get specific project information
    whose pid is passed in path parameter
"""
@router.get("/api/projectdata-by-pid/{pid}")
def getProjectByPidApi(pid: str):
    return getProjectByPid(pid)


"""
    api which will get specific project
    information whose name is passed in path parameter
"""
@router.get("/api/projectdata-by-projectname/{project_name}")
def getProjectByProjectNameApi(project_name: str):
    return getProjectByProjectName(project_name)


"""
    api which will update project details by pmo
"""
@router.patch("/api/update-project-details-pmo/{pid}")
def updateProjectDetailsPmoApi(UpdateDetailsObj: ProjectUpdationByPmo, pid: str) -> int:
    return updateProjectDetailsPmo(UpdateDetailsObj, pid)


"""
    api which will update project details by pm
"""
@router.patch("/api/update-project-details-pm/{pid}")
def updateProjectDetailsPmApi(UpdateDetailsObj: ProjectUpdationByPm, pid: str) -> int:
    return updateProjectDetailsPm(UpdateDetailsObj, pid)

@router.patch("/api/create-update-team/{pid}")
def createUpdateTeamApi(req_obj: Dict, pid:str):
    return createUpdateTeam(req_obj, pid)