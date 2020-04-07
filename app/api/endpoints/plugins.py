from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from ...utils.jira_plugin import get_all_jira_projects, get_project_keys
from ...crud.jira_plugin import sync_jira_with_database
from ...crud.dropdowns import get_dropdowns

router = APIRouter()

"""
    api to sync projects with JIRA
"""
@router.get("/sync/{sync_name}")
def return_jira_projects(sync_name: str):
    if sync_name == 'jira':
        sync_jira_with_database()
        return "success"
    else:
        raise HTTPException(404, f"{sync_name} is not valid parameter")

@router.get("/all-dropdowns")
def return_dropdowns():
    return get_dropdowns()