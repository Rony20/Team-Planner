from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

from ...security.auth import create_new_token, get_current_user
from ...models.auth import User, TokenData

router = APIRouter()
security = HTTPBasic()

#login api for user.

@router.get("/login", response_model=TokenData)
def login_api(credentials: HTTPBasicCredentials = Depends(security)):
   return create_new_token(credentials.username, credentials.password)
   