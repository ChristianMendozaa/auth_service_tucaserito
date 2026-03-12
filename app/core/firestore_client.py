import json
from google.cloud import firestore
from google.oauth2 import service_account
from app.core.config import settings

_client = None

def get_firestore_client() -> firestore.Client:
    global _client
    if _client is None:
        creds_info = json.loads(settings.GOOGLE_CREDENTIALS_JSON)
        creds = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=[
                "https://www.googleapis.com/auth/datastore",
                "https://www.googleapis.com/auth/cloud-platform"
            ]
        )
        _client = firestore.Client(project=settings.project_id, credentials=creds)
    return _client
