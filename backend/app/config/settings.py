from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    BSF_MODE: str = "SIMULATION"
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_LOG_LEVEL: str = "info"
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"

    SECRET_KEY: str = "bsf_secret_dev_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "bsf_monitor"
    POSTGRES_USER: str = "bsf_user"
    POSTGRES_PASSWORD: str = "bsf_sim_password"
    DATABASE_URL: str = "postgresql+asyncpg://bsf_user:bsf_sim_password@postgres:5432/bsf_monitor"

    MQTT_HOST: str = "mosquitto"
    MQTT_PORT: int = 1883
    MQTT_KEEPALIVE: int = 60
    MQTT_CLIENT_ID: str = "bsf_backend_service"
    MQTT_USER: str = ""
    MQTT_PASSWORD: str = ""

    CAMERA_MODE: str = "VIRTUAL"
    STORAGE_PATH: str = "/app/storage/media"
    IMAGE_CAPTURE_INTERVAL: int = 300
    MEDIA_MAX_FILE_SIZE_MB: int = 50

    SIMULATION_TICK_RATE_SECONDS: int = 5
    SIMULATION_NOISE_LEVEL: float = 0.05
    SENSOR_POLL_INTERVAL: int = 5

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(
        env_file=".env.simulation",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
