from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from typing import List
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


class PastProjects(BaseModel):
    '''This class saves Past Projects with name and worked hours'''

    project: str
    worked_hours: int


class CurrentProjects(BaseModel):
    '''This class saves Current Projects with name and worked hours'''

    project: str
    allocation: List[int] = []
    @validator("allocation")
    def check_allocation_hours(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
            return value


class Employee(BaseModel):
    '''This class saves Employee details'''

    employee_id: int
    employee_name: str
    designation: str
    skills: List[str] = None
    past_projects: List[PastProjects] = None
    current_projects: List[CurrentProjects] = None
    availability: List[int] = []
    @validator("availability")
    def check_availability_hours(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
            return value

    is_allocated: bool


class UpdateEmployee(BaseModel):
    '''This class saves a model which is sent by Client while updatation'''

    employee_id: int = None
    designation: str = None
    past_projects: PastProjects = None
    current_projects: CurrentProjects = None
    skills: str = None
    availability: List[int] = None
    @validator("availability")
    def check_availability_hours(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
            return value

    is_allocated: bool = None
