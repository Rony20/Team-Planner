from ..db.mongodb_utils import DatabaseConnector, Collections
from enum import Enum

db_connector = DatabaseConnector()

class UserRoles(str, Enum):
    "This class contails roles for accesing application endpoints"

    APPROVER = 'Approver'
    LEAD = "Lead"
    USER = "User"

def get_user_role(employee_id) -> str:
    """
    :param employee_id: unique id of employee.
    :type employee_id: int
    :return: role of employee based on his designation.
    :rtype: str
    """

    PMO = ["PMO Analyst"]
    PM = ["Technical Lead", "Senior Technical Lead", "Technical Project Manager, Engineering", "Technical Project Manager, Managed Services",
          "Senior Technical Project Manager, Engineering", "Quality Assurance Lead", ]
    employee = db_connector.collection(Collections.EMPLOYEES).find_one(
        {"employee_id": employee_id}, {"_id": 0, "designation": 1})

    designation = employee["designation"]

    if designation in PMO:
        return UserRoles.APPROVER
    elif designation in PM:
        return UserRoles.LEAD
    else:
        return UserRoles.USER