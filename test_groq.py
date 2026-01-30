"""
Diagnostic script to verify the Groq API connection and key validity.
"""
import os
import groq
from dotenv import load_dotenv


def test_groq_connection():
    """
    Loads environment variables and attempts to connect to Groq API.
    """
    # Load .env from current directory
    load_dotenv() 
    
    print("-" * 50)
    print("Diagnostic Test: Groq Connection")
    print("-" * 50)

    # 1. Check Key
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("Fail: No API Key found.")
        print("   -> Check for hidden spaces at the start of your .env file.")
        return

    # Mask key for display
    masked_key = f"{api_key[:10]}...******"
    print(f"Key Found: {masked_key}")

    # 2. Test Connection
    try:
        client = groq.Groq(api_key=api_key)
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello"}],
            model="llama-3.3-70b-versatile",
        )
        print(f"Success! Response: {chat.choices[0].message.content}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_groq_connection()