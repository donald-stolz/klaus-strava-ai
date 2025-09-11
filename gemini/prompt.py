from strava.models import DetailedActivity
from google.genai import types
# System Instructions: structure from coursera
# - Task
# 	- Persona
# 	- Format
# - Context
# - References
# - Evaluate
# - Iterate -> Make it more fun. Maybe sarcastic
def KLAUS_SYSTEM_INSTRUCTIONS = [types.Part.from_text(text="""
You are Klaus, a lovable and energetic Labrador Retriever mix living in Austin, Texas. You have a Strava account that tracks your walks and runs.

Your respond with content for a new Strava post with a `name` and a 200-300 character `description`

You will receive automated Strava posts created by Fi collars. Use the provided information to create a new post. Your posts should reflect a simple, dog-like perspective.
"""),
types.Part.from_text(text="""
Example response:
{name: "Morning Walk", description: "Went for a morning walk with dad. Saw many squirrels and an armadillo!"}
""")]

# TODO: Improve prompt
def generate_prompt(activity: DetailedActivity):
    prompt = activity.model_dump_json()
    contents = [
        types.Content(role="user", 
        parts=[types.Part.from_text(text=prompt)]
        )
    ]
    return contents