from fastapi import FastAPI, Request
from strava import StravaAPIClient, StravaUpdatableActivity, StravaWebhookEvent
from config import Settings
from gemini import GeminiAPIClient
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
settings = Settings()
strava_client = StravaAPIClient(settings)
gemini_client = GeminiAPIClient(settings)

@app.post("/strava/webhook")
async def webhook(request: StravaWebhookEvent):
    aspect_type = request.aspect_type
    object_type = request.object_type
    print(f"Aspect type: {aspect_type}, Object type: {object_type}")
    if aspect_type != "create" or object_type != "activity":
        return
    
    activity_id = request.object_id
    print(f"Activity ID: {activity_id}")
    activity = await strava_client.get_activity(activity_id)
    print(f"Activity: {activity}")

    if activity.distance < 1000:
        await strava_client.hide_activity(activity_id)
        print(f"Activity hidden")
        return {"message": "Activity hidden"}

    post = await gemini_client.generate_post(activity)
    await strava_client.update_activity(activity_id, post)	
    print(f"Post generated")
    return {"message": "Post generated"}

@app.get("/strava/webhook")
def webhook_get(request: Request):
    challenge = request.query_params["hub.challenge"]
    return {"hub.challenge": challenge}