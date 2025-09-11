from fastapi import FastAPI
from strava import StravaAPIClient, StravaUpdatableActivity
from config import Settings

settings = Settings()
app = FastAPI()
strava_client = StravaAPIClient(settings)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/strava/athlete")
def get_athlete():
    return strava_client.get_athlete()

@app.get("/strava/activities")
def get_activities():
    return strava_client.get_activities()

@app.get("/strava/activity/{activity_id}")
def get_activity(activity_id: str):
    return strava_client.get_activity(activity_id)

@app.put("/strava/activity/{activity_id}")
def update_activity(activity_id: str, activity: StravaUpdatableActivity):
    return strava_client.update_activity(activity_id, activity)

@app.put("/strava/activity/{activity_id}/hide")
def hide_activity(activity_id: str):
    return strava_client.hide_activity(activity_id)