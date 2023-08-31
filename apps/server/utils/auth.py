from typing import Tuple
import gql.transport.exceptions
from fastapi import HTTPException, Request
from api.client import L3Api
from fastapi.security import OAuth2PasswordBearer
from api.user import User
from api.account import Account
from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from typings.auth import UserAccount
from datetime import timedelta, datetime
from config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate(request: Request) -> Tuple[User, Account]:
    try:
        api = L3Api(request.headers, request.cookies)
        user = api.user.fetch_user()
        account = api.account.fetch_account()
        # return user, account
        return UserAccount(user=user, account=account)
    except gql.transport.exceptions.TransportQueryError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

def generate_token(user_email, jwt_authorizer: AuthJWT = Depends()):
    token_config = Config.JWT_EXPIRY
    if type(token_config) == str:
        token_config = int(token_config)
    if token_config is None:
        token_config = 300
    token_expiry_time = timedelta(hours=token_config)
    token = jwt_authorizer.create_access_token(subject=user_email, expires_time=token_expiry_time)
    return token
