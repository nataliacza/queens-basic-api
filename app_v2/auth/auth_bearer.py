from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            payload = decode_jwt(credentials.credentials)
            if payload["scope"] == "access_token":
                return credentials.credentials
            raise HTTPException(status_code=403, detail="Scope for the token is invalid")
        raise HTTPException(status_code=403, detail="Invalid authorization token.")
