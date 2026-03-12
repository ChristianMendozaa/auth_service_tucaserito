from typing import Optional
from pydantic import BaseModel


class GoogleTokenRequest(BaseModel):
    id_token: str


class UserResponse(BaseModel):
    google_id: str
    email: str
    name: str
    picture: str
    created_at: str
    last_login: str
    is_active: bool
    is_new_user: bool


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MeResponse(BaseModel):
    google_id: str
    email: str
    name: str
    picture: str
    is_active: bool
