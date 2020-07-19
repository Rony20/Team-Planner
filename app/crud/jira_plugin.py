from datetime import (
    datetime,
    date,
    timedelta
)
from typing import List

from ..db.mongodb_utils import DatabaseConnector, Collections
from ..utils.jira_plugin import get_project_keys, get_all_jira_projects
from ..crud.projects import create_project,update_existing_project_on_jirasync
from ..crud.dropdowns import get_pm_list
from ..utils.logger import Logger
from fastapi.exceptions import HTTPException


db_connector = DatabaseConnector()
logger = Logger()


def get_pm_id(name):
    pm_list = get_pm_list()

    for pm in pm_list:
        if pm["value"] == name:
            return pm["code"]


def extract_keys_from_database() -> List:
    """
    This method will fetch all projects keys from database
    and return the list of keys.

    :return: Return a list of string keys.
    :rtype: List
    """

    database_epics = db_connector.collection(Collections.PROJECTS).find({}, {
        "_id": 0, "epic_id": 1})
    database_key_list = list()
    for epic in database_epics:
        database_key_list.append(epic["epic_id"])
    return database_key_list


def get_epic_keys() -> List:
    """
    This method will fetch all projects keys from jira
    and compare them with database keys. This will return
    the list of keys which are available in JIRA but
    not in Database.

    :return: Return a list of string keys.
    :rtype: List
    """
    untracked_key_list = list()
    common_keys_list = list()

    jira_key_list = get_project_keys()
    database_key_list = extract_keys_from_database()
    untracked_key_list = list(set(jira_key_list) - set(database_key_list))
    common_keys_list = list(set(jira_key_list) & set(database_key_list))

    return untracked_key_list,common_keys_list


def insert_project_into_database(project) -> None:
    """
    This method is kind of mapper method. It will
    convert project argument into database acceptable
    project format and stores project in database.

    :rtype: None
    """

    #project_object = {
    #    'project_id': project["project_id"],
    #    'project_name': project["project_name"],
    #    'assigned_pm': get_pm_id(project["assigned_pm"]),
    #    'start_date': "",
    #    'end_date': "",
    #    'allocated_employees': [],
    #    'status': project["status"],
    #    'skillset': [],
    #    'description': ""
    #}

    create_project(project)

def update_project_in_database(project) -> None:
    """
    """
    project_details = {}
    project_details['logged_hours'] = project['logged_hours']
    project_details['status'] = project['status']
    project_details['end_date'] = project['end_date']
    project_details['epic_type'] = project['epic_type']
    epic_id = project['epic_id']

    update_project = update_existing_project_on_jirasync(project_details,epic_id)


def sync_jira_with_database() -> None:
    """
    This methods will only allow the projects to be
    stored in database which are in JIRA projects but
    not in database.
    """

    untracked_keys, common_keys = get_epic_keys()
    logger.info(f"JIRA projects successfully fetched.")

    if len(common_keys) != 0:
        list_of_common_projects = get_all_jira_projects(common_keys)

        for common_project in list_of_common_projects:
            update_project_in_database(common_project)
    logger.info(f"Existing projects updated successfully.")

    if len(untracked_keys) != 0:
        list_of_jira_projects = get_all_jira_projects(untracked_keys)

        for project in list_of_jira_projects:
            insert_project_into_database(project)
    logger.info(f"JIRA sync successfully done.")
