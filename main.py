from fastapi import FastAPI
from strava.client import StravaAPIClient

app = FastAPI()
strava_client = StravaAPIClient()

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