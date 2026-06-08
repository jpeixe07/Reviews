from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Reviews API"
    mongodb_url: str
    mongodb_db: str = "reviews_db"
    mongodb_tls: bool = True  # Atlas needs TLS; set false for a local/Docker Mongo

    jwt_secret: str = "dev-insecure-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()