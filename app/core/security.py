import json
import requests
from google.oauth2 import service_account
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional

from app.core.config import settings

def get_gcp_credentials():
    creds_info = json.loads(settings.GOOGLE_CREDENTIALS_JSON)
    return service_account.Credentials.from_service_account_info(
        creds_info,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

def verify_google_id_token(id_token: str) -> dict:
    """
    Validates a Google ID Token using Google's public certs endpoint.
    Returns the decoded payload with user info (sub, email, name, picture).
    Raises ValueError if the token is invalid.
    """
    # Fetch Google's public certs
    certs_url = "https://www.googleapis.com/oauth2/v3/certs"
    response = requests.get(certs_url)
    response.raise_for_status()
    certs = response.json()

    # Use google-auth to verify the token
    from google.oauth2 import id_token as google_id_token
    from google.auth.transport import requests as google_requests

    request = google_requests.Request()
    try:
        payload = google_id_token.verify_oauth2_token(
            id_token,
            request,
            settings.GOOGLE_CLIENT_ID
        )
    except Exception as e:
        raise ValueError(f"Token de Google inválido: {str(e)}")

    return payload

def create_access_token(user_id: str, email: str) -> str:
    """Creates an internal JWT for session management."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "app": "tu-caserito"
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates an internal JWT. Returns payload or None."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
