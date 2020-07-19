import requests
import json
import concurrent.futures
import datetime
import re

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from typing import Dict, List
from html.parser import HTMLParser
from ..crud.dropdowns import get_pm_list
from fastapi.exceptions import HTTPException

from ..core.config import (
    JIRA_URL,
    JIRA_EPICS_URL,
    JIRA_EPIC,
    JIRA_USER,
    JIRA_PASSWORD
)
from ..utils.logger import Logger

logger =Logger()

def get_pm_id(name):
    pm_list = get_pm_list()

    for pm in pm_list:
        if pm["value"] == name:
            return pm["code"]


def get_project_keys() -> List:
    """
    get_project_key() method crates a list of keys by
    fetching list of projects from JIRA api.

    :return: List of string keys for projects.
    :rtype: list
    """
    try:
        response = requests.get(JIRA_EPICS_URL, auth=(JIRA_USER, JIRA_PASSWORD))
        if response.status_code == 500:
            logger.error("Invalid Credentials ! Couldn't connect to JIRA.")
    except requests.exceptions.ConnectionError as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=502, detail="Connection Error !")
    except requests.exceptions.Timeout as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=408, detail="Request Timeout !")
    except requests.exceptions.TooManyRedirects as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=310, detail="Too many redirects !")
    except requests.exceptions.RequestException as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=300, detail=ex)
    else:
        epic_keys = list()
        epics = json.loads(response.text)
        epic_issues = epics['issues']
        for issue in epic_issues:
            epic_key = issue['key']
            if epic_key != None:
                epic_keys.append(epic_key)

        return epic_keys


def get_status(status_category, start_date, end_date) -> str:
    """
    """
    status_string = ''
    if status_category == 'Closed':
        status_string += 'Complete'
    else:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        current_date = datetime.datetime.now()
        difference_start_end = (end_date - start_date).days

        if current_date <= end_date:
            difference_start_current = (current_date - start_date).days
            complete_percentage = int((difference_start_current/difference_start_end)*100)
            status_string += 'OnTrack: {}% complete'.format(complete_percentage)
        else:
            difference_current_today = (current_date - end_date).days
            delayed_percentage = int((difference_current_today/difference_start_end)*100)
            status_string += 'Delayed by {}%'.format(delayed_percentage)
    return status_string


def get_project_from_jira(key) -> Dict:
    """
    get_project_from_jira method takes key as argument and retrives
    corrosponding project detail from JIRA api.

    :param key: Unique key for JIRA project.
    :type key: str
    :return: Return a Dict object having fields projec_id,
     project_name, assigned_pm and status.
    :rtype: Dict
    """
    try:
        new_response = requests.get(
            JIRA_EPIC+'/'+key, auth=(JIRA_USER, JIRA_PASSWORD))
        if new_response.status_code == 500:
            logger.error("Invalid Credentials ! Couldn't connect to JIRA.")
    except requests.exceptions.ConnectionError as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=502, detail="Connection Error !")
    except requests.exceptions.Timeout as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=408, detail="Request Timeout !")
    except requests.exceptions.TooManyRedirects as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=310, detail="Too many redirects !")
    except requests.exceptions.RequestException as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=300, detail=ex)
    else:
        new_epic = json.loads(new_response.text)
        new_epic_details = {}

        project = new_epic['fields']['project']
        if project != None:
            new_epic_details['project_name'] = project['name']
            new_epic_details['project_id'] = project['key']
        else:
            new_epic_details['project_name'] = 'No Value'
            new_epic_details['project_id'] = 'No Value'
        
        epic_key = new_epic['key']
        if epic_key != None:
            new_epic_details['epic_id'] = epic_key
        else:
            new_epic_details['epic_id'] = 'No Value'

        epic_name = new_epic['fields']['customfield_10002']
        if epic_name != None:    
            new_epic_details['epic_name'] = epic_name
        else:
            new_epic_details['epic_name'] = "No Value"
        
        project_lead = new_epic['fields']['customfield_11112']
        if project_lead != None:
            project_lead_coc = get_pm_id(project_lead['displayName'])
            new_epic_details['assigned_pm'] = project_lead_coc
        else:
            new_epic_details['assigned_pm'] = -1

        dev_team = new_epic['fields']['customfield_11129']
        if dev_team != None:
            display_names = []
            for index in dev_team:
                dev_name = index['displayName']
                display_names.append(dev_name)               
            new_epic_details['allocated_developers'] = display_names
        else:
            new_epic_details['allocated_developers'] = [] 
        
        qa_team = new_epic['fields']['customfield_11130']
        if qa_team != None:
            display_names_qa = []
            for qa in qa_team:
                qa_name = qa['displayName']
                display_names_qa.append(qa_name)               
            new_epic_details['allocated_qa'] = []
        else:
            new_epic_details['allocated_qa'] = 'No Value'

        qa_lead = new_epic['fields']['customfield_11134']
        if qa_lead != None:
            new_epic_details['allocated_qalead'] = qa_lead['displayName']
        else:
            new_epic_details['allocated_qalead'] = 'No Value'

        customer_name = new_epic['fields']['customfield_11117']
        if customer_name != None:
            new_epic_details['customer_name'] = customer_name['value']
        else:
            new_epic_details['customer_name'] = 'No Value'

        bd_estimated = new_epic['fields']['customfield_11128']
        if bd_estimated != None:
            new_epic_details['bd_estimated'] = bd_estimated
        else:
            new_epic_details['bd_estimated'] = 'No Value'

        pmo_estimated = new_epic['fields']['customfield_11127']
        if pmo_estimated != None:
            new_epic_details['pmo_estimated'] = pmo_estimated
        else:
            new_epic_details['pmo_estimated'] = 'No Value'

        pmo_start = new_epic['fields']['customfield_11106']
        if pmo_start != None:
            new_epic_details['start_date'] = pmo_start
        else:
            new_epic_details['start_date'] = 'No Value'

        pmo_end = new_epic['fields']['customfield_11107']
        if pmo_end != None:
            new_epic_details['end_date'] = pmo_end
        else:
            new_epic_details['end_date'] = 'No Value'
        
        summary = new_epic['fields']['summary']
        if summary != None:
            new_epic_details['description'] = summary
        else:
            new_epic_details['description'] = 'No Value'

        logged_hours_html = new_epic['fields']['customfield_11110']
        if logged_hours_html != None:
            pattern = re.compile(r'<strong>(.*?)</strong>')
            logged_hours = pattern.search(logged_hours_html).group(1)
            new_epic_details['logged_hours'] = logged_hours
        else:
            new_epic_details['logged_hours'] = 'No Value'

        epic_status = new_epic['fields']['status']
        if epic_status != None and pmo_start!= None and pmo_end != None:
            status_category = epic_status['name']
            new_epic_details['status'] = get_status(status_category,pmo_start,pmo_end)
        else:
            new_epic_details['status'] = 'No Value'
        
        if epic_status != None:
            new_epic_details['epic_type'] = epic_status['name']
        else:
            new_epic_details['epic_type'] = 'No Value'

        new_epic_details['skillset'] = []

        return new_epic_details


def get_all_jira_projects(list_of_project_keys) -> List:
    """
    get_all_jira_projects method takes list of projects keys as argument
    and fetch deetail for every project from jira project corrosponding to
    it's key.

    :param list_of_project_keys: list of unique key for JIRA project.
    :type list_of_project_keys: List
    :return: Return a list of Dict object having fields
     projec_id, project_name, assigned_pm and status.
    :rtype: List
    """

    projects_list = list()

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(list_of_project_keys)) as executor:
        future_to_url = {executor.submit(
            get_project_from_jira, key): key for key in list_of_project_keys}
        for future in concurrent.futures.as_completed(future_to_url):
            projects_list.append(future.result())

    return projects_list
