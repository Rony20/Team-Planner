from datetime import (
    datetime,
    date,
    timedelta
)
from typing import List

from ..db.mongodb_utils import DatabaseConnector, Collections
from ..utils.jira_plugin import get_project_keys, get_all_jira_projects
from ..crud.projects import createProject

db_connector = DatabaseConnector()


def extract_keys_from_database() -> List:
    """
    This method will fetch all projects keys from database
    and return the list of keys.

    :return: Return a list of string keys.
    :rtype: List
    """

    projects = db_connector.collection(Collections.PROJECTS).find({}, {
        "_id": 0, "project_id": 1})

    database_key_list = list()
    for project in projects:
        database_key_list.append(project["project_id"])
    return database_key_list


def get_untracked_keys() -> List:
    """
    This method will fetch all projects keys from jira
    and compare them with database keys. This will return
    the list of keys which are available in JIRA but
    not in Database.

    :return: Return a list of string keys.
    :rtype: List
    """

    untracked_key_list = list()

    jira_key_list = get_project_keys()
    database_key_list = extract_keys_from_database()

    untracked_key_list = list(set(jira_key_list) - set(database_key_list))
    return untracked_key_list


def insert_project_into_database(project) -> None:
    """
    This method is kind of mapper method. It will
    convert project argument into database acceptable
    project format and stores project in database.

    :rtype: None
    """

    project_object = {
        'project_id': project["project_id"],
        'project_name': project["project_name"],
        'assigned_pm': project["assigned_pm"],
        'status': project["status"],
    }

    createProject(project_object)


def sync_jira_with_database() -> None:
    """
    This methods will only allow the projects to be
    stored in database which are in JIRA projects but
    not in database.
    """

    untracked_keys = get_untracked_keys()
    if len(untracked_keys) != 0:
        list_of_jira_projects = get_all_jira_projects(untracked_keys)

        for project in list_of_jira_projects:
            insert_project_into_database(project)
    else:
        pass
