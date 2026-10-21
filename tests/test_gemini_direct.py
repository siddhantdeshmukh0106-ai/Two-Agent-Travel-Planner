import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=api_key)

print("Testing Gemini API directly...\n")

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello in one sentence."
    )

    print("Gemini Response:")
    print(response.text)

except Exception as error:
    print("Gemini API Error:")
    print(error)