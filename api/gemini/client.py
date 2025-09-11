from google import genai
from google.genai import types
from .models import GeminiSettings, GeminiPost
from strava.models import DetailedActivity
from .prompt import KLAUS_SYSTEM_INSTRUCTIONS, generate_prompt
import json

class GeminiAPIClient:   
    def __init__(self, settings: GeminiSettings):
        self.gemini_api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model_name
        self.client = genai.Client(api_key=self.gemini_api_key)
    
    def generate_content_config(self):
        config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=-1,
            ),
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["name", "description"],
                properties = {
                    "name": genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                    "description": genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                },
            ),
            system_instruction = KLAUS_SYSTEM_INSTRUCTIONS
        )
        return config

    def generate_post(self, activity: DetailedActivity):
        contents = generate_prompt(activity)
        content_config = self.generate_content_config()

        # Generate post
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=contents,
            config=content_config
        )
        
        # Send response JSON
        response_json = json.loads(response.text)
        return GeminiPost(**response_json)
