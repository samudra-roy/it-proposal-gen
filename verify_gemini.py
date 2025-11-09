# verify_gemini.py
# Purpose: check that .env is loaded and Gemini responds.
from dotenv import load_dotenv
import os
from google import genai

# 1️⃣ Load .env file (brings your API key into Python)
load_dotenv()

# 2️⃣ Read the key from the environment
api_key = os.getenv("GOOGLE_API_KEY")
print("Step 1: API Key found?", bool(api_key))

# 3️⃣ Create a Gemini client using that key
client = genai.Client(api_key=api_key)

# 4️⃣ Test prompt (short and cheap)
prompt = "Give one short idea for an AI tool that helps IT teams in India."

# 5️⃣ Send the prompt to Gemini
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# 6️⃣ Print the response text
print("Step 2: Gemini said:", response.text)