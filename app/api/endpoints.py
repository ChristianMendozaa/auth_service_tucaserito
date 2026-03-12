import logging
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.schemas import GoogleTokenRequest, AuthResponse, UserResponse, MeResponse
from app.core.security import verify_google_id_token, create_access_token, decode_access_token
from app.services.user_service import get_or_create_user, get_user_by_id

logger = logging.getLogger(__name__)
router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/google", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def google_auth(request: GoogleTokenRequest):
    """
    Accepts a Google ID Token from the frontend.
    Verifies it with Google, then auto-registers or logs in the user in Firestore.
    Returns an internal JWT access token + user info.
    """
    try:
        # 1. Verify the Google ID token
        google_payload = verify_google_id_token(request.id_token)

        # 2. Get or create the user in Firestore
        user_data = get_or_create_user(google_payload)

        # 3. Create our internal JWT
        access_token = create_access_token(
            user_id=user_data["google_id"],
            email=user_data["email"]
        )

        user_response = UserResponse(
            google_id=user_data["google_id"],
            email=user_data["email"],
            name=user_data["name"],
            picture=user_data["picture"],
            created_at=user_data["created_at"],
            last_login=user_data["last_login"],
            is_active=user_data["is_active"],
            is_new_user=user_data["is_new_user"],
        )

        action = "registrado" if user_data["is_new_user"] else "autenticado"
        logger.info(f"Usuario {action}: {user_data['email']}")

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    except ValueError as e:
        logger.warning(f"Token de Google inválido: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error en autenticación Google: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la autenticación."
        )


@router.get("/me", response_model=MeResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Protected endpoint. Validates the internal JWT and returns the current user's profile.
    Requires header: Authorization: Bearer <access_token>
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    google_id = payload.get("sub")
    user_data = get_user_by_id(google_id)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    if not user_data.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada."
        )

    return MeResponse(
        google_id=user_data["google_id"],
        email=user_data["email"],
        name=user_data["name"],
        picture=user_data["picture"],
        is_active=user_data["is_active"],
    )
