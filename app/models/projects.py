from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict
from datetime import datetime


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
    skillset: List[int] = None


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


class AllocationForProject(BaseModel):
    """
    AllocationForProject class contains attributes which store
    information about employee's weekly allocation
    """

    week: List[datetime] = None
    hours: List[int] = None


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

    assigned_pm: int = None
    @validator("assigned_pm")
    def validate_assigned_pm(cls, value):
        if not isinstance(value, int):
            raise ValueError("Invalid : value should be integer")
        return value

    start_date: datetime = None
    end_date: datetime = None
    allocated_employees: Dict[str, List[AllocationForProject]] = None
    status: bool
    skillset: List[int]
    description: str = None
