from typing import Optional, Dict, Any
import httpx
from .models import DetailedActivity, StravaUpdatableActivity, StravaAPIError, StravaConfig


class StravaAPIClient:
	def __init__(self, settings: StravaConfig):
		self.client_id = settings.strava_client_id
		self.client_secret = settings.strava_client_secret
		self.refresh_token = settings.strava_refresh_token
		self.base_url = settings.strava_base_url
		self.access_token: Optional[str] = None

	def refresh_access_token(self):
		url = f"{self.base_url}/oauth/token"
		data = {
			"client_id": self.client_id,
			"client_secret": self.client_secret,
			"grant_type": "refresh_token",
			"refresh_token": self.refresh_token
		}
		response = httpx.post(url, data=data)
		self.access_token = response.json()["access_token"]
		self.refresh_token = response.json()["refresh_token"]
  
	def check_access_token(self):
		# TODO: Check if the access token is expired
		if not self.access_token:
			self.refresh_access_token()
  
	def get_athlete(self):
		self.check_access_token()
		url = f"{self.base_url}/athlete"
		response = httpx.get(url, headers={"Authorization": f"Bearer {self.access_token}"})
		return response.json()
  
	def get_activities(self):
		self.check_access_token()
		url = f"{self.base_url}/activities"
		response = httpx.get(url, headers={"Authorization": f"Bearer {self.access_token}"})
		return response.json()

	def get_activity(self, activity_id: str) -> DetailedActivity:
		"""Get a detailed activity by ID."""
		self.check_access_token()
		url = f"{self.base_url}/activities/{activity_id}"
		response = httpx.get(url, headers={"Authorization": f"Bearer {self.access_token}"})
		
		if response.status_code != 200:
			raise StravaAPIError(
				f"Failed to get activity {activity_id}: {response.text}",
				status_code=response.status_code,
				response_data=response.json() if response.text else None
			)
		
		return DetailedActivity(**response.json())

	def update_activity(self, activity_id: str, activity: StravaUpdatableActivity) -> DetailedActivity:
		"""Update an activity with the provided data."""
		self.check_access_token()
		url = f"{self.base_url}/activities/{activity_id}"
		
		# Convert Pydantic model to dict, excluding None values
		activity_data = activity.model_dump(exclude_none=True)
		
		response = httpx.put(url, headers={"Authorization": f"Bearer {self.access_token}"}, json=activity_data)
		
		if response.status_code != 200:
			raise StravaAPIError(
				f"Failed to update activity {activity_id}: {response.text}",
				status_code=response.status_code,
				response_data=response.json() if response.text else None
			)
		
		return DetailedActivity(**response.json())

	def hide_activity(self, activity_id: str) -> DetailedActivity:
		"""Hide an activity from the home feed."""
		activity_update = StravaUpdatableActivity(hide_from_home=True)
		return self.update_activity(activity_id, activity_update)