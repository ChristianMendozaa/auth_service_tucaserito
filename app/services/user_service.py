import logging
from datetime import datetime, timezone
from typing import Optional

from google.cloud import firestore
from app.core.firestore_client import get_firestore_client

logger = logging.getLogger(__name__)

USERS_COLLECTION = "users"


def get_or_create_user(google_payload: dict) -> dict:
    """
    Looks up the user by their Google ID (sub claim).
    - If found: updates last_login, returns user with is_new_user=False.
    - If not found: creates new document, returns user with is_new_user=True.
    """
    db = get_firestore_client()
    collection = db.collection(USERS_COLLECTION)

    google_id = google_payload.get("sub")
    if not google_id:
        raise ValueError("Token de Google no contiene un ID de usuario (sub).")

    doc_ref = collection.document(google_id)
    doc = doc_ref.get()

    now = datetime.now(timezone.utc).isoformat()

    if doc.exists:
        # Existing user — update last_login
        doc_ref.update({
            "last_login": now
        })
        user_data = doc.to_dict()
        user_data["is_new_user"] = False
        logger.info(f"Login existente: {user_data.get('email')} ({google_id})")
        return user_data
    else:
        # New user — create document
        user_data = {
            "google_id": google_id,
            "email": google_payload.get("email", ""),
            "name": google_payload.get("name", ""),
            "picture": google_payload.get("picture", ""),
            "created_at": now,
            "last_login": now,
            "is_active": True,
        }
        doc_ref.set(user_data)
        user_data["is_new_user"] = True
        logger.info(f"Nuevo usuario registrado: {user_data.get('email')} ({google_id})")
        return user_data


def get_user_by_id(google_id: str) -> Optional[dict]:
    """Fetches a user document from Firestore by their Google ID."""
    db = get_firestore_client()
    doc = db.collection(USERS_COLLECTION).document(google_id).get()
    if doc.exists:
        return doc.to_dict()
    return None
