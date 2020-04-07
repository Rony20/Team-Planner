from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict
from datetime import datetime


class AllocationForProject(BaseModel):
    """
    AllocationForProject class contains attributes which store
    information about employee's weekly allocation
    """

    week: List[datetime] = None
    hours: List[int] = None


class AllocatedEmployees(BaseModel):
    """
    AllocatedEmployees represents employees under a specific project

    :param BaseModel: inhertitence from BaseModel
    :type BaseModel: class
    """
    employee_id: int
    status: bool
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
    start_date: datetime = None
    end_date: datetime = None
    allocated_employees: List[AllocatedEmployees] = []
    skillset: List[int] = None


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
    start_date: datetime = ""
    end_date: datetime = ""
    allocated_employees: List[AllocatedEmployees] = []
    status: bool
    skillset: List[int] = []
    description: str = ""
