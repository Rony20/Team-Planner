from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient, ReturnDocument
from fastapi.encoders import jsonable_encoder
from typing import List, Dict
from datetime import *
from ..db.mongodb_utils import DatabaseConnector, Collections
from ..models.requests import (
    Request,
    UpdateRequestByPM,
    UpdateRequestByPMO
)

db_connector = DatabaseConnector()
date_regex = r"(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-]\d{4}"


def make_new_request(request: Request) -> bool:
    """
    make_new_request method takes request object as argument and creates a new request in the database. Only PM can access this method while creating a new request.

    :param request: Request object having data members like request_id, pm_id, project_id, request_date, requested employees,...etc.
    :type request: Request
    :return: result of the operation in boolean.
    :rtype: bool
    """
    request_object = dict(request)
    if str(request_object["employee_id"]) not in request_object["request_id"].split("-")[1]:
        raise HTTPException(status_code=422,
                            detail="Invalid: request id does not match with employee id.")
    elif request_object["project_id"] not in (request_object["request_id"].split("-"))[0]:
        raise HTTPException(status_code=422,
                            detail="Invalid: request id does not match with project id.")

    request_document = db_connector.collection(
        Collections.REQUESTS).insert_one(request_object)
    return request_document.acknowledged


def get_all_requests() -> list:
    """
    get_all_requests method takes no arguments and return all requests to the User.
    Only PMO will be able to access this method while approving or rejecting requests.

    :return: return list of all requests made during this week.
    :rtype: list
    """
    all_requests = []
    for request_object in db_connector.collection(
            Collections.REQUESTS).find({}, {"_id": False}):
        all_requests.append(request_object)
    return all_requests


def get_requests_by_pm(pm_id: int, week_start: str = Query(..., regex=date_regex) , week_end: str = Query(..., regex=date_regex)) -> list:
    """
    get_requests_by_pm method takes id of pm as argument and return
    a list of requests made by pm in all projects.

    :return: list of requests made by pm.
    :rtype: list
    """
    all_requests = []
    requested_week = [week_start, week_end]
    my_query = {"pm_id": pm_id, "requested_week": requested_week}
    for request_object in db_connector.collection(
            Collections.REQUESTS).find((my_query), {"_id": False}):
        all_requests.append(request_object)
    return all_requests


def approve_reject_request_by_pmo(request_id: str, updateRequest: UpdateRequestByPMO) -> dict:
    """
    approve_reject_request_by_pmo method takes request_id and pm_id
    as argument and returns the boolean value of the operation performed.
    This method is accessible only by PMO.
    PMO can approve/ reject the request.
    Based on the result the status of request is changed
    to either approved or declined

    :param request_id: represents unique request present inside the collection.
    :type request_id: string
    :param pm_id: represents the PMO who is managing the request.
    :type pm_id: string
    :return: result of the operation in boolean.
    :rtype: bool
    """
    my_query = {"request_id": request_id}
    request_document = db_connector.collection(
        Collections.REQUESTS).find_one_and_update(
            my_query,
            {
                "$set": jsonable_encoder(updateRequest)
            },
            projection={"_id": False},
            return_document=ReturnDocument.AFTER
    )
    return request_document
