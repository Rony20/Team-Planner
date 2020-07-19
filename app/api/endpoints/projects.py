from fastapi import APIRouter, Depends
from typing import List, Dict
from fastapi.exceptions import HTTPException

from ...crud.projects import (
    update_project_details_pmo,
    update_project_details_pm,
    get_project_by_name,
    get_project_by_pid,
    create_project,
    get_all_project_details,
    create_update_team
)

from ...models.projects import (
    ProjectUpdationByPmo,
    ProjectUpdationByPm,
    Project,
    AllocationForProject,
)

from ...models.auth import User
from ...utils.role_manager import UserRoles
from ...security.auth import lead_approver_permission

router = APIRouter()

"""
    api which create new project
"""
@router.post("/api/create-project/")
def create_project_api(project: Project, user: User = Depends(lead_approver_permission)) -> bool:
    return create_project(project)


"""
    api which will get all projects information
"""
@router.get("/api/all-project-details")
def get_all_project_details_api(user: User = Depends(lead_approver_permission)):
    return get_all_project_details()


"""
    api which will get specific project information
    whose pid is passed in path parameter
"""
@router.get("/api/projectdata-by-pid/{pid}")
def get_project_by_pid_api(pid: str, user: User = Depends(lead_approver_permission)):
    return get_project_by_pid(pid)


"""
    api which will get specific project
    information whose name is passed in path parameter
"""
@router.get("/api/projectdata-by-projectname/{project_name}")
def get_project_by_name_api(project_name: str, user: User = Depends(lead_approver_permission)):
    return get_project_by_name(project_name)


"""
    api which will update project details by pmo
"""
@router.patch("/api/update-project-details-pmo/{pid}")
def update_project_details_pmo_api(update_details_obj: ProjectUpdationByPmo, pid: str, user: User = Depends(lead_approver_permission)) -> int:
    return update_project_details_pmo(update_details_obj, pid)


"""
    api which will update project details by pm
"""
@router.patch("/api/update-project-details-pm/{pid}")
def update_project_details_pm_api(update_details_obj: ProjectUpdationByPm, pid: str, user: User = Depends(lead_approver_permission)) -> int:
    return update_project_details_pm(update_details_obj, pid)


@router.patch("/api/create-update-team/{pid}")
def create_update_team_api(req_obj: Dict, pid: str, user: User = Depends(lead_approver_permission)):
    return create_update_team(req_obj, pid)
