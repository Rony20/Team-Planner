import requests
import json

from dotenv import load_dotenv
from fastapi import HTTPException

from .logger import Logger
from ..core.config import HRMS_USER, ENCRYPTED_PASSWORD, LOGIN_URL, GRAPHQL_URL


# Graphql queries
SKILL_LIST = "{\"query\":\"query{allSkill}\",\"variables\":{}}"
DESIGNATION_LIST = "{\"query\":\"query{allDropdown(cocCode:\\\"12\\\") {code value}}\",\"variables\":{}}"
TECHONOLOGY_LIST = "{\"query\":\"query{allTechnology}\",\"variables\":{}}"
USERS_LIST = "{\"query\":\"query{\\nemployeeSkillDetails{\\n...on EmployeeSkillsList{\\nEmployeeSkillsList\\n{empCode\\ndesignation\\nname\\nemail\\nrole\\nskill\\nprimaryTechnology\\nsecondaryTechnology\\n\\n}\\n\\n}\\n...on AuthInfoField{message}\\n\\n}\\n\\n}\",\"variables\":{}}"

logger = Logger()


def get_graphql_response(query, token):
    ''' get graphql json response '''
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': 'application/json'
    }
    payload = query
    try:
        logger.info("Getting data from HRMS.")
        response = requests.request(
            "POST", GRAPHQL_URL, headers=headers, data=payload)
        if response.status_code == 500:
            logger.error(
                "Token Mismatch detected ! Couldn't connect to HRMS.")
            raise HTTPException(
                status_code=500, detail="Token Mismatch detected ! Couldn't connect to HRMS.")
    except requests.exceptions.ConnectionError as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=502, detail="Connection Error !")
    except requests.exceptions.Timeout as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=408, detail="Request Timeout !")
    except requests.exceptions.TooManyRedirects as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=310, detail="Too many redirects !")
    except Exception as ex:
        logger.error(repr(ex))
        raise HTTPException(status_code=300, detail=ex)
    else:
        return response.json()


def get_auth_token():
    ''' get auth token '''
    payload = {
        "username": HRMS_USER,
        "password": ENCRYPTED_PASSWORD
    }
    payload = json.dumps(payload)
    headers = {
        'Content-Type': 'text/plain'
    }
    try:
        logger.info("Getting authentication token...")
        response = requests.request(
            "POST", LOGIN_URL, headers=headers, data=payload)
        if response.status_code == 500:
            logger.error("Invalid Credentials ! Couldn't connect to HRMS.")
            raise HTTPException(
                status_code=500, detail="Invalid Credentials ! Couldn't connect to HRMS.")
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
        auth_data = response.json()
        return auth_data.get('token')
