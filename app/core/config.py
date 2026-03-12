import json
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CREDENTIALS_JSON: str
    GCS_BUCKET_NAME: str = ""
    GOOGLE_CLOUD_REGION: str = "us-central1"
    GOOGLE_CLIENT_ID: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    @property
    def project_id(self) -> str:
        creds = json.loads(self.GOOGLE_CREDENTIALS_JSON)
        return creds.get("project_id", "")

    class Config:
        env_file = ".env"

settings = Settings()
