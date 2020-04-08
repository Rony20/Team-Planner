from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict
from datetime import datetime
import re

date_regex = re.compile(r"^((19)\d\d|2\d\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[0-1])$")

def validate_date(value):
    """
    validate_date method validates the date for YYYY-MM-DD format
    
    :param value: date to be validated
    :type value: string
    :return: bool value if date satisfies the regex
    :rtype: bool
    """
    if not date_regex.fullmatch(value):
        return True
    else:
        return False


class AllocationForProject(BaseModel):
    """
    AllocationForProject class contains attributes which store
    information about employee's weekly allocation
    """
    week: List[str] = None
    hours: List[int] = None


class AllocatedEmployees(BaseModel):
    """
    AllocatedEmployees represents employees under a specific project

    :param BaseModel: inhertitence from BaseModel
    :type BaseModel: class
    """
    employee_id: int
    status: str 
    allocation: List[AllocationForProject]


class ProjectUpdationByPm(BaseModel):
    """
    ProjectUpdationByPm class has all atributes which can be modify by Pm
    """

    project_name: str = None
    @validator("project_name")
    def validate_name(cls, value):
        if value == "":
            raise ValueError("Invalid : ProjectName cannot be empty")
        return value
    technologies: List[str] = None


class ProjectUpdationByPmo(BaseModel):
    """
    ProjectUpdationByPmo class has all attributes which can be changed by pmo
    """

    project_name: str = None
    @validator("project_name")
    def validate_name(cls, value):
        if value == "":
            raise ValueError("Invalid : ProjectName cannot be empty")
        return value
    assigned_pm: int = None
    start_date: str = None
    end_date: str = None
    allocated_employees: List[AllocatedEmployees] = []
    skillset: List[int] = None
    @validator("start_date")
    def validate_date(cls, value):
        if(not validate_date(value)):
            raise ValueError("Invalid Date format.") 
    @validator("end_date")
    def validate_date2(cls, value):
        if(not validate_date(value)):
            raise ValueError("Invalid Date format.") 


class Project(BaseModel):
    """
    Project class contain all information related to
    project along with all allocation which is made in past
    """
    project_id: str
    project_name: str
    @validator("project_name")
    def validate_name(cls, value):
        if value == "":
            raise ValueError("Invalid : ProjectName cannot be empty")
        return value
    assigned_pm: int = 0
    start_date: str = ""
    end_date: str = ""
    allocated_employees: List[AllocatedEmployees] = []
    status: bool
    skillset: List[int] = []
    description: str = ""
    @validator("start_date")
    def validate_date(cls, value):
        if(not validate_date(value)):
            raise ValueError("Invalid Date format.") 
    @validator("end_date")
    def validate_date2(cls, value):
        if(not validate_date(value)):
            raise ValueError("Invalid Date format.") 