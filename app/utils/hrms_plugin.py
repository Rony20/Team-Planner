import requests
import os
import json

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv('.env')

HRMS_USER = os.getenv("HRMS_USER")
ENCRYPTED_PASSWORD = os.getenv("ENCRYPTED_PASS")

# read from core config with env var
LOGIN_URL = os.getenv("LOGIN_URL")
GRAPHQL_URL = os.getenv("GRAPHQL_URL1")

# Graphql queries
SKILL_LIST = "{\"query\":\"query{allSkill}\",\"variables\":{}}"
DESIGNATION_LIST = "{\"query\":\"query{allDropdown(cocCode:\\\"12\\\") {code value}}\",\"variables\":{}}"
TECHONOLOGY_LIST = "{\"query\":\"query{allTechnology}\",\"variables\":{}}"
USERS_LIST = "{\"query\":\"query{\\nemployeeSkillDetails{\\n...on Employeelist{\\nEmployeelist\\n{empCode\\ndesignation\\nname\\nskill\\nprimaryTechnology\\nsecondaryTechnology\\n\\n}\\n\\n}\\n...on AuthInfoField{message}\\n\\n}\\n\\n}\",\"variables\":{}}"


def get_graphql_response(query, token):
    ''' get graphql json response '''
    headers = {
        'Authorization': "Bearer " + token,
        'Content-Type': 'application/json'
    }
    payload = query
    try:
        response = requests.request(
            "POST", GRAPHQL_URL, headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Connection Error !")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request Timeout !")
    except requests.exceptions.TooManyRedirects:
        raise HTTPException(status_code=310, detail="Too many redirects !")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=300, detail=e)
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
        response = requests.request(
            "POST", LOGIN_URL, headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=502, detail="Connection Error !")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request Timeout !")
    except requests.exceptions.TooManyRedirects:
        raise HTTPException(status_code=310, detail="Too many redirects !")
    except requests.exceptions.RequestException as e:
        raise HTTPException(detail=e)
    else:
        auth_data = response.json()
        return auth_data.get('token')
