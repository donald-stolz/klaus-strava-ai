from fastapi import FastAPI
from strava import StravaAPIClient, StravaUpdatableActivity
from config import Settings
from gemini import GeminiAPIClient
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
settings = Settings()
strava_client = StravaAPIClient(settings)
gemini_client = GeminiAPIClient(settings)

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

@app.put("/gemini/post/{activity_id}")
def generate_post(activity_id: str):
    activity = strava_client.get_activity(activity_id)
    post = gemini_client.generate_post(activity)
    strava_client.update_activity(activity_id, post)
    return post