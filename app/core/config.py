from datetime import datetime
from typing import Optional

from pydantic import BaseSettings, EmailStr

FORMAT = "%Y/%m/%d %H:%M:%S"


class Settings(BaseSettings):
    app_title: str = 'Приложение QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    now_date_time = datetime.now().strftime(FORMAT)

    class Config:
        env_file = '.env'


settings = Settings()