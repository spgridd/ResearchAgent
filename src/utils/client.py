from dotenv import load_dotenv
import os
import google.genai as genai

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
USE_VERTEXAI = True

def get_client():
    client = genai.Client(
        vertexai=USE_VERTEXAI,
        project=PROJECT_ID,
        location=LOCATION
    )

    return client