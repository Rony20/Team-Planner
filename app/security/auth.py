import jwt
from jwt import PyJWTError

from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from ..utils.ad_connection import ADConnector
from ..db.mongodb_utils import DatabaseConnector, Collections
from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRES_MINUTES
from ..models.auth import User, TokenData
from ..utils.role_manager import UserRoles, get_user_role


ad_connector = ADConnector()
db_connector = DatabaseConnector()
expires_delta = ACCESS_TOKEN_EXPIRES_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_user_name(employee_id) -> str:
    """
    :param employee_id: unique id of employee.
    :type employee_id: int
    :return: name of employee.
    :rtype: str
    """

    employee = db_connector.collection(Collections.EMPLOYEES).find_one(
        {"employee_id": employee_id}, {"_id": 0, "employee_name": 1})
    return employee["employee_name"]


def create_new_token(username, password) -> TokenData:
    """
    Generate new authentication token.

    :param username: username from the request header.
    :type username: str
    :param password: password from the request header.
    :type password: str
    :return: fresh created token along with sone user information.
    :rtype: TokenData
    """

    ad_response = ad_connector.check_ad_authentication(username, password)

    is_validate = ad_response["is_validate"]
    if is_validate:
        employee_id = ad_response["employee_id"]

        role = get_user_role(employee_id)
        name = get_user_name(employee_id)
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)

        token_data = {
            "username": username,
            "employee_id": employee_id,
            "exp": expire
        }

        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        data_to_return = {
            "id": employee_id,
            "name": name,
            "role": role,
            "token": token
        }

        return data_to_return

    else:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Returns currently login user by checkking token validity
    details. And raise exceptions if user token is not valid.

    :param token: extracted token from request header.
    :type token: str
    :return: detail about login user using token.
    :rtype: User
    """

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        username: str = payload.get("username")
        employee_id: int = payload.get("employee_id")
        if username is None or employee_id is None:
            raise credential_exception
    except PyJWTError:
        raise credential_exception
    check_user_detail = ad_connector.check_user_status(username, employee_id)
    if not check_user_detail["is_user"]:
        raise credential_exception
    else:
        if not check_user_detail["active"]:
            raise HTTPException(status_code=400, detail="Inactive User !")
    user = User(username=username, id=employee_id, name=get_user_name(
        employee_id), role=get_user_role(employee_id), active=True)

    return user

#def lead_approver_permission(user: User = Depends(get_current_user)) -> User:
def lead_approver_permission():
    """
    This method will prevent normal users from accesing
    some API endpoints.

    :param role: role of employee.
    :type role: Enum UserRoles
    """

    #if user.role == UserRoles.USER:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail="Service is not permissable for you!")
    #return user
    pass

def approver_permission(user: User = Depends(get_current_user)) -> User:
    if user.role == UserRoles.LEAD or user.role == UserRoles.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Service is not permissable for you!")
    return user