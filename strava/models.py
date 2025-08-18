from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, Field


@dataclass
class StravaConfig:
    """Configuration for Strava API integration."""
    client_id: str
    client_secret: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    base_url: str = "https://www.strava.com/api/v3"


class StravaPost(BaseModel):
    """Pydantic model for Strava post/activity data."""
    id: int = Field(..., description="Unique identifier for the post")
    name: str = Field(..., description="Name/title of the activity")
    description: Optional[str] = Field(None, description="Description of the activity")
    distance: Optional[float] = Field(None, description="Distance in meters")
    moving_time: Optional[int] = Field(None, description="Moving time in seconds")
    elapsed_time: Optional[int] = Field(None, description="Total elapsed time in seconds")
    total_elevation_gain: Optional[float] = Field(None, description="Total elevation gain in meters")
    type: Optional[str] = Field(None, description="Type of activity")
    start_date: Optional[datetime] = Field(None, description="Start date of the activity")
    created_at: Optional[datetime] = Field(None, description="When the activity was created")
    updated_at: Optional[datetime] = Field(None, description="When the activity was last updated")

class StravaAPIError(Exception):
    """Custom exception for Strava API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)
