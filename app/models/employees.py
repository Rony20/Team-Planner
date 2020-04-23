from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, ValidationError, validator
from typing import List
from fastapi.exceptions import RequestValidationError


class AllocationForProject(BaseModel):
    """
    AllocationForProject stores allocation of employee in project

    :param BaseModel: BaseModel class
    :type BaseModel: class
    :raises ValueError: checks the range of hour
    """
    week: List[str] = None
    hours: List[int] = None
    @validator("hours")
    def check_availability_hours(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
        return value


class Availability(BaseModel):
    """
    Availability stores availability of employee for current and next week in hours

    :param BaseModel: BaseModel class
    :type BaseModel: class
    :raises ValueError: checks the range of hour
    :raises ValueError: checks the range of hour
    """
    current_week: List[int] = []
    next_week: List[int] = []
    @validator("current_week")
    def check_availability_hours(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
        return value

    @validator("next_week")
    def check_availability_hours2(cls, value):
        for hour in value:
            if hour < 0 or hour > 8:
                raise ValueError("Invalid: hours should be in range (0-8).")
        return value


class PastProjects(BaseModel):
    '''This class saves Past Projects with name and worked hours'''

    project_id: str
    worked_hours: int


class CurrentProjects(BaseModel):
    '''This class saves Current Projects with name and worked hours'''

    project_id: str
    allocation: List[AllocationForProject] = []


class Employee(BaseModel):
    '''This class saves Employee details'''

    employee_id: int
    employee_name: str
    designation: str
    skills: List[int] = None
    past_projects: List[PastProjects] = None
    current_projects: List[CurrentProjects] = None
    availability: List[Availability] = []
    is_allocated: bool


class UpdateEmployee(BaseModel):
    '''This class saves a model which is sent by Client while updatation'''

    designation: str = None
    past_projects: PastProjects = None
    current_projects: CurrentProjects = None
    skills: List[int] = None
    availability: List[Availability] = None
    is_allocated: bool = None
