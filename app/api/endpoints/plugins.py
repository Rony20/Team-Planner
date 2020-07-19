from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from ...utils.jira_plugin import get_all_jira_projects, get_project_keys
from ...crud.jira_plugin import sync_jira_with_database
from ...crud.hrms_plugin import sync_hrms_with_database
from ...crud.dropdowns import get_dropdowns
from ...security.auth import lead_approver_permission, get_current_user
from ...models.auth import User

router = APIRouter()

"""
    api to sync projects with JIRA
"""
#def return_jira_projects(sync_name: str, user: User = Depends(lead_approver_permission)):
@router.get("/sync/{sync_name}")
def return_jira_projects(sync_name: str):
    if sync_name == 'jira':
        sync_jira_with_database()
        return "success"
    if sync_name == 'hrms':
        sync_hrms_with_database()
        return "success"
    else:
        raise HTTPException(404, f"{sync_name} is not valid parameter")

@router.get("/all-dropdowns")
def return_dropdowns():
    return get_dropdowns()