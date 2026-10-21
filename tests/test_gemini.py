import os
from dotenv import load_dotenv
from crewai import LLM

# Step 1: Load environment variables
load_dotenv()

# Step 2: Retrieve Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env file!")

# Step 3: Initialize Gemini through CrewAI
llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=api_key,
    temperature=0.7
)

# Step 4: Send a test prompt
print("Connecting to Google Gemini...\n")

response = llm.call(
    messages=[
        {
            "role": "user",
            "content": "Suggest three famous tourist attractions in Jaipur, India. Keep your answer short."
        }
    ]
)

# Step 5: Display the response
print("Gemini Response:\n")
print(response)