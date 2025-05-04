from typing import List, Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 5487
    log_level: str = "info"
    refresh_rate: int = 10
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000"]
    mock_max_fan_cooling: int = 10
    mock_temperature_range: Tuple[int, int] = (20, 50)
    mock_temperature_threshold: int = 45
    mock_offline_chance_threshold: float = 0.01

    model_config = SettingsConfigDict(env_file=".env", env_prefix="ROBOT_API_")

settings = Settings()
