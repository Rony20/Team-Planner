from pydantic import BaseModel
from enum import Enum

class User(BaseModel):
    """
    This clsss is user model which will give currently
    login user details from the token.
    """

    username: str
    id: int
    name: str
    role: str
    active: bool

class TokenData(BaseModel):
    """
    This class is token model which will return some
    information about user who is logged in along with
    token.
    """

    id: int
    name: str
    role: str
    token: str

class UserRoles(str, Enum):
    "This class contails roles for accesing application endpoints"

    APPROVER = 'Approver'
    LEAD = "Lead"
    USER = "User"