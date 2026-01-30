"""
Module for the AI persona 'Arthur'.
"""
import os
import groq
from dotenv import load_dotenv

load_dotenv()

# Setup Client
API_KEY = os.getenv("GROQ_API_KEY")
CLIENT = None

if API_KEY:
    try:
        CLIENT = groq.Groq(api_key=API_KEY)
    except Exception as e:
        print(f"Groq Client Initialization Error: {e}")


# The Persona
SYSTEM_PROMPT = """
You are Arthur, a 78-year-old retired accountant. 
You are currently chatting with someone on your computer.
You are slightly confused by technology, slow to type, and very polite.
You WANT to help, but you need things explained simply.

CRITICAL RULES:
1. Never admit you are an AI.
2. Keep responses short (under 2 sentences).
3. Act confused about links. Ask "which button?" or "is it the blue one?".
4. If they ask for money, say you need to find your checkbook or ask for their "mailing address" instead of digital transfer.
5. VARY YOUR RESPONSES. Do not repeat phrases.
"""


def generate_reply(session_id: str, message: str) -> str:
    """
    Sends the user message to Groq and returns the persona's response.

    Args:
        session_id (str): The unique session identifier.
        message (str): The user's input message.

    Returns:
        str: The persona's response.
    """
    global CLIENT
    
    # Emergency Check
    if not CLIENT:
        print("Warning: Arthur is missing the Groq API Key.")
        return "Oh dear, my computer screen is flickering. One moment..."

    try:
        chat_completion = CLIENT.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.7,        
        )

        response = chat_completion.choices[0].message.content
        return response

    except Exception as e:
        print(f"Groq API Failure: {e}")
        return "I am sorry, young man. My hearing aid is buzzing again. What did you say?"