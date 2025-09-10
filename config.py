from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
    strava_client_id: str
    strava_client_secret: str
    strava_refresh_token: str
    strava_base_url: str = "https://www.strava.com/api/v3"
