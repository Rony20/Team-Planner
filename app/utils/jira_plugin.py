import requests
import json
import concurrent.futures

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from typing import Dict, List

from ..core.config import (
    JIRA_URL,
    JIRA_USER, 
    JIRA_PASSWORD
)


def get_project_keys() -> List:
    """
    get_project_key() method crates a list of keys by fetching list of projects from JIRA api.

    :return: List of string keys for projects.
    :rtype: list
    """

    response = requests.get(JIRA_URL, auth=(JIRA_USER, JIRA_PASSWORD))
    project_keys = list()
    
    projects = json.loads(response.text)

    for project in projects:
        project_keys.append(project['key'])

    return project_keys


def get_project_from_jira(key) -> Dict:
    """
    get_project_from_jira method takes key as argument and retrives
    corrosponding project detail from JIRA api.

    :param key: Unique key for JIRA project.
    :type key: str
    :return: Return a Dict object having fields projec_id, project_name, assigned_pm and status.
    :rtype: Dict
    """

    new_response = requests.get(JIRA_URL+'/'+key, auth=(JIRA_USER, JIRA_PASSWORD))
    project_details = json.loads(new_response.text)

    new_project_details = {
        "project_id": project_details["key"],
        "project_name": project_details["name"],
        "assigned_pm": project_details["lead"]["displayName"],
        "status": not project_details["archived"]
    }
    return new_project_details    

def get_all_jira_projects(list_of_project_keys) -> List:
    """
    get_all_jira_projects method takes list of projects keys as argument
    and fetch deetail for every project from jira project corrosponding to
    it's key.

    :param list_of_project_keys: list of unique key for JIRA project.
    :type list_of_project_keys: List
    :return: Return a list of Dict object having fields projec_id, project_name, assigned_pm and status.
    :rtype: List
    """

    projects_list = list()

    with concurrent.futures.ThreadPoolExecutor(max_workers= len(list_of_project_keys)) as executor:
        future_to_url = { executor.submit(get_project_from_jira, key): key for key in list_of_project_keys}
        for future in concurrent.futures.as_completed(future_to_url):
            projects_list.append(future.result())
    
    return projects_list
