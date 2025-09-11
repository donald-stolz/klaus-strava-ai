from pydantic import BaseModel

class GeminiSettings:
    gemini_api_key: str
    gemini_model_name: str = "gemini-2.5-flash"
    
class GeminiPost(BaseModel):
    name: str
    description: str