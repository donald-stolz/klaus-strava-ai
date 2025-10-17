# klaus-strava-ai

A fun AI impersonation of my dog connected to Strava. Takes the automated posts from the walks with my dog's Fi collar and generates more entertaining descriptions.

Uses [FastAPI](https://fastapi.tiangolo.com/) and [Google Gemini](https://ai.google.dev/gemini-api/docs). 

### TODO

- [x] Authenticate with Strava API
- [x] Strava class to handle API calls
- [x] AWS lambda
- [ ] Webhook subscription for new strava activities
- [ ] Hide short walks
- [ ] Gemini AI class to generate messages for the post
  - [x] LLM in Google AI Studio
  - [ ] Save chat history or give llm other activity context
  - [x] Response schema; Title, description

`fastapi dev api/main.py`
