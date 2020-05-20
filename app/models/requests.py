from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from typing import List, Dict
from datetime import datetime
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


class Request(BaseModel):
    """
    Request class represents the request made by PM for next week allocation.
    Only PM will be accessing this class while making a new request.
    Whenever a new request is created, its status will be set to pending.
    all the fields are necessary except description.
    This will be a base class for all requests.
    Here request_id is of this format: project_id + employee_id + request_date

    :param BaseModel: BaseModel class
    :type BaseModel: class
    """

    request_id: str
    project_id: str
    pm_id: int
    employee_id: int
    requested_week: List[str]
    requested_hours: List[int]
    priority: str
    request_status = "pending"
    request_date: str
    pmo_id = 0

    @validator("requested_hours")
    def check_requested_hours(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
        return value

    @validator("priority")
    def check_priority(cls, value):
        if value not in ["Urgent", "Medium"]:
            raise ValueError(
                "Invalid: Priority should be either 'Urgent' or 'Medium'.")
        return value

    @validator("requested_week")
    def check_requested_week(cls, value):
        for week in value:
            if not datetime.strptime(week, '%d-%m-%Y'):
                raise ValueError(
                    "Invalid! Date format should be dd-mm-yyyy")
        return value

    @validator("request_date")
    def check_requested_date(cls, value):
        if not datetime.strptime(value, '%d-%m-%Y'):
            raise ValueError(
                "Invalid! Date format should be dd-mm-yyyy")
        return value


class UpdateRequestByPM(BaseModel):
    """
    UpdateRequest represent the updation required in the already created request.
    PMO will be able to access it.
    When two or more PM requests for the same employee, 
    system will change request status to conflicted and alert the PM as well.

    :param BaseModel: BaseModel class
    :type BaseModel: class
    """
    pass


class UpdateRequestByPMO(BaseModel):
    """
    UpdateRequestByPMO represents the updation required in the already created request.
    PMO will be able to access it when he/she approves or rejects the request.

    :param BaseModel: BaseModel class
    :type BaseModel: class
    """
    pmo_id: int
    request_status: str
    @validator("request_status")
    def check_status(cls, value):
        if value not in ["pending", "declined", "approved"]:
            raise ValueError(
                "Invalid: status field should be pending, declined or rejected.")
        return value
