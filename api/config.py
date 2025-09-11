from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')
    strava_client_id: str
    strava_client_secret: str
    strava_refresh_token: str
    strava_base_url: str = "https://www.strava.com/api/v3"
    gemini_api_key: str
    gemini_model_name: str = "gemini-2.5-flash"
