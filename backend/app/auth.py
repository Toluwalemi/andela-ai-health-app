from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer

from app.config import get_settings

_clerk_guard = ClerkHTTPBearer(ClerkConfig(jwks_url=get_settings().clerk_jwks_url))


def current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(_clerk_guard),
) -> str:
    user_id = creds.decoded.get("sub") if creds and creds.decoded else None
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    return user_id
