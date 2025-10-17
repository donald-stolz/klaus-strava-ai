from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

class StravaConfig:
    """Configuration for Strava API integration."""
    client_id: str
    client_secret: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    base_url: str = "https://www.strava.com/api/v3"


class StravaAPIError(Exception):
    """Custom exception for Strava API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


# Supporting Models for DetailedActivity
class PolylineMap(BaseModel):
    """Represents a polyline map."""
    id: str = Field(..., description="The identifier of the map")
    polyline: Optional[str] = Field(None, description="The polyline of the map")
    summary_polyline: Optional[str] = Field(None, description="The summary polyline of the map")


class MetaAthlete(BaseModel):
    """Meta representation of an athlete."""
    id: int = Field(..., description="The unique identifier of the athlete")
    resource_state: int = Field(..., description="Resource state, indicates level of detail")


class PhotosSummary(BaseModel):
    """Summary of photos associated with an activity."""
    count: int = Field(..., description="The number of photos")
    primary: Optional[Dict[str, Any]] = Field(None, description="The primary photo")


class SummaryGear(BaseModel):
    """Summary representation of gear."""
    id: str = Field(..., description="The gear's unique identifier")
    resource_state: int = Field(..., description="Resource state")
    primary: bool = Field(..., description="Whether this gear is the athlete's default for this activity type")
    name: str = Field(..., description="The gear's name")
    distance: float = Field(..., description="The distance logged with this gear")


class DetailedSegmentEffort(BaseModel):
    """Detailed representation of a segment effort."""
    id: int = Field(..., description="The unique identifier of this effort")
    resource_state: int = Field(..., description="Resource state")
    name: str = Field(..., description="The name of the segment on which this effort was performed")
    elapsed_time: int = Field(..., description="Time in seconds")
    moving_time: int = Field(..., description="Time in seconds")
    start_date: datetime = Field(..., description="The time at which the effort was started")
    start_date_local: datetime = Field(..., description="The time at which the effort was started in local time")
    distance: float = Field(..., description="The effort's distance in meters")
    start_index: int = Field(..., description="The start index of this effort in its activity's stream")
    end_index: int = Field(..., description="The end index of this effort in its activity's stream")
    average_cadence: Optional[float] = Field(None, description="The effort's average cadence")
    average_watts: Optional[float] = Field(None, description="The average wattage of this effort")
    device_watts: Optional[bool] = Field(None, description="For riding efforts, whether the wattage was reported by a dedicated recording device")
    average_heartrate: Optional[float] = Field(None, description="The heart heart rate of the athlete during this effort")
    max_heartrate: Optional[float] = Field(None, description="The maximum heart rate of the athlete during this effort")


class Split(BaseModel):
    """Represents a split for an activity."""
    distance: float = Field(..., description="The distance of this split, in meters")
    elapsed_time: int = Field(..., description="The elapsed time of this split, in seconds")
    elevation_difference: float = Field(..., description="The elevation difference of this split, in meters")
    moving_time: int = Field(..., description="The moving time of this split, in seconds")
    split: int = Field(..., description="N/A")
    average_speed: float = Field(..., description="The average speed of this split, in meters per second")
    pace_zone: Optional[int] = Field(None, description="The pace zone of this split")


class Lap(BaseModel):
    """Represents a lap of an activity."""
    id: int = Field(..., description="The unique identifier of this lap")
    resource_state: int = Field(..., description="Resource state")
    name: str = Field(..., description="The name of the lap")
    elapsed_time: int = Field(..., description="The lap's elapsed time, in seconds")
    moving_time: int = Field(..., description="The lap's moving time, in seconds")
    start_date: datetime = Field(..., description="The time at which the lap was started")
    start_date_local: datetime = Field(..., description="The time at which the lap was started in the local timezone")
    distance: float = Field(..., description="The lap's distance, in meters")
    start_index: int = Field(..., description="The start index of this effort in its activity's stream")
    end_index: int = Field(..., description="The end index of this effort in its activity's stream")
    lap_index: int = Field(..., description="The index of this lap in the activity it belongs to")
    max_speed: float = Field(..., description="The maximum speed of this lap, in meters per second")
    average_speed: float = Field(..., description="The average speed of this lap, in meters per second")
    average_cadence: Optional[float] = Field(None, description="The lap's average cadence")
    average_watts: Optional[float] = Field(None, description="The average wattage of this lap")
    average_heartrate: Optional[float] = Field(None, description="The average heart rate of the athlete during this lap")
    max_heartrate: Optional[float] = Field(None, description="The maximum heart rate of the athlete during this lap")
    total_elevation_gain: float = Field(..., description="The lap's total elevation gain")


# https://developers.strava.com/docs/reference/#api-models-UpdatableActivity
class StravaUpdatableActivity(BaseModel):
    """Updatable activity fields for Strava API."""
    hide_from_home: Optional[bool] = Field(None, description="Whether to hide the activity from home feed")
    name: Optional[str] = Field(None, description="The name of the activity")
    description: Optional[str] = Field(None, description="The description of the activity")
    commute: Optional[bool] = Field(None, description="Whether this activity is a commute")
    trainer: Optional[bool] = Field(None, description="Whether this activity is a trainer activity")
    gear_id: Optional[str] = Field(None, description="Identifier for the gear used during the activity")


# https://developers.strava.com/docs/reference/#api-models-DetailedActivity
class DetailedActivity(BaseModel):
    """
    Detailed representation of a Strava activity.
    Based on: https://developers.strava.com/docs/reference/#api-models-DetailedActivity
    """
    id: int = Field(..., description="The unique identifier of the activity")
    resource_state: int = Field(..., description="Resource state, indicates level of detail")
    external_id: Optional[str] = Field(None, description="The identifier provided at upload time")
    upload_id: Optional[int] = Field(None, description="The identifier of the upload that resulted in this activity")
    athlete: MetaAthlete = Field(..., description="An instance of MetaAthlete")
    name: str = Field(..., description="The name of the activity")
    distance: float = Field(..., description="The activity's distance, in meters")
    moving_time: int = Field(..., description="The activity's moving time, in seconds")
    elapsed_time: int = Field(..., description="The activity's elapsed time, in seconds")
    total_elevation_gain: float = Field(..., description="The activity's total elevation gain")
    type: str = Field(..., description="Deprecated. Prefer to use sport_type")
    sport_type: str = Field(..., description="An instance of SportType")
    start_date: datetime = Field(..., description="The time at which the activity was started")
    start_date_local: datetime = Field(..., description="The time at which the activity was started in the local timezone")
    timezone: str = Field(..., description="The timezone of the activity")
    utc_offset: float = Field(..., description="The UTC offset of the activity in seconds")
    location_city: Optional[str] = Field(None, description="The city where the activity took place")
    location_state: Optional[str] = Field(None, description="The state where the activity took place")
    location_country: Optional[str] = Field(None, description="The country where the activity took place")
    achievement_count: int = Field(..., description="The number of achievements gained during this activity")
    kudos_count: int = Field(..., description="The number of kudos given for this activity")
    comment_count: int = Field(..., description="The number of comments for this activity")
    athlete_count: int = Field(..., description="The number of athletes for taking part in a group activity")
    photo_count: int = Field(..., description="The number of Instagram photos for this activity")
    map: PolylineMap = Field(..., description="An instance of PolylineMap")
    trainer: bool = Field(..., description="Whether this activity is a trainer activity")
    commute: bool = Field(..., description="Whether this activity is a commute")
    manual: bool = Field(..., description="Whether this activity was created manually")
    private: bool = Field(..., description="Whether this activity is private")
    flagged: bool = Field(..., description="Whether this activity is flagged")
    workout_type: Optional[int] = Field(None, description="The activity's workout type")
    upload_id_str: Optional[str] = Field(None, description="The unique identifier of the upload in string format")
    average_speed: float = Field(..., description="The activity's average speed, in meters per second")
    max_speed: float = Field(..., description="The activity's max speed, in meters per second")
    has_kudoed: bool = Field(..., description="Whether the logged-in athlete has kudoed this activity")
    hide_from_home: bool = Field(..., description="Whether the activity is muted")
    gear_id: Optional[str] = Field(None, description="The id of the gear for the activity")
    kilojoules: Optional[float] = Field(None, description="The total work done in kilojoules during this activity. Rides only")
    average_watts: Optional[float] = Field(None, description="Average power output in watts during this activity. Rides only")
    device_watts: Optional[bool] = Field(None, description="Whether the watts are from a power meter, false if estimated")
    max_watts: Optional[int] = Field(None, description="Rides with power meter data only")
    weighted_average_watts: Optional[int] = Field(None, description="Similar to Normalized Power. Rides with power meter data only")
    description: Optional[str] = Field(None, description="The description of the activity")
    photos: Optional[PhotosSummary] = Field(None, description="An instance of PhotosSummary")
    gear: Optional[SummaryGear] = Field(None, description="An instance of SummaryGear")
    calories: Optional[float] = Field(None, description="The number of kilocalories consumed during this activity")
    segment_efforts: Optional[List[DetailedSegmentEffort]] = Field(None, description="A collection of DetailedSegmentEffort objects")
    device_name: Optional[str] = Field(None, description="The name of the device used to record the activity")
    embed_token: Optional[str] = Field(None, description="The token used to embed a Strava activity")
    splits_metric: Optional[List[Split]] = Field(None, description="The splits of this activity in metric units (for runs)")
    splits_standard: Optional[List[Split]] = Field(None, description="The splits of this activity in imperial units (for runs)")
    laps: Optional[List[Lap]] = Field(None, description="A collection of Lap objects")
    best_efforts: Optional[List[DetailedSegmentEffort]] = Field(None, description="A collection of DetailedSegmentEffort objects")
    
    # Additional fields that might be present
    start_latlng: Optional[List[float]] = Field(None, description="The activity's start coordinates")
    end_latlng: Optional[List[float]] = Field(None, description="The activity's end coordinates")
    pr_count: Optional[int] = Field(None, description="The number of personal records achieved during this activity")
    total_photo_count: Optional[int] = Field(None, description="The total number of photos for this activity")
    has_heartrate: Optional[bool] = Field(None, description="Whether the activity has heart rate data")
    average_heartrate: Optional[float] = Field(None, description="The average heart rate during the activity")
    max_heartrate: Optional[float] = Field(None, description="The maximum heart rate during the activity")
    heartrate_opt_out: Optional[bool] = Field(None, description="Whether the athlete has opted out of heart rate sharing")
    display_hide_heartrate_option: Optional[bool] = Field(None, description="Whether to display the heart rate hide option")
    elev_high: Optional[float] = Field(None, description="The activity's highest elevation, in meters")
    elev_low: Optional[float] = Field(None, description="The activity's lowest elevation, in meters")
    average_cadence: Optional[float] = Field(None, description="The average cadence during the activity")
    average_temp: Optional[int] = Field(None, description="The average temperature during the activity, in celsius")
    perceived_exertion: Optional[int] = Field(None, description="The perceived exertion for the activity")
    prefer_perceived_exertion: Optional[bool] = Field(None, description="Whether the athlete prefers perceived exertion over other metrics")
    segment_leaderboard_opt_out: Optional[bool] = Field(None, description="Whether the athlete has opted out of segment leaderboards")
    leaderboard_opt_out: Optional[bool] = Field(None, description="Whether the athlete has opted out of leaderboards")

class StravaWebhookEvent(BaseModel):
    """Represents a Strava webhook event."""
    object_type: str = Field(..., description="The type of the object")
    object_id: int = Field(..., description="The ID of the object")
    aspect_type: str = Field(..., description="The type of the aspect")
    updates: Optional[Dict[str, Any]] = Field(None, description="The updates to the object")
    owner_id: int = Field(..., description="The ID of the owner of the object")
    subscription_id: int = Field(..., description="The ID of the subscription")
    event_time: datetime = Field(..., description="The time of the event")