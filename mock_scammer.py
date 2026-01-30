"""
Standalone script to simulate a scammer interacting with the API.
"""
import os
import time
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_URL = "http://127.0.0.1:8000/chat"
API_KEY = os.getenv("API_SECRET_KEY", "your_secret_key_here")


def simulate_scam():
    """Runs a simulated scam conversation loop."""
    session_id = str(uuid.uuid4())
    print(f"--- Starting Simulation [Session: {session_id}] ---")

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    # Scenario: Prince Scam
    messages = [
        "Hello, this is urgent. I am Prince Al-Waleed. I need your bank details to transfer $5M. Visit http://prizecenter.bad/claim",
        "Why is it taking so long? Please verify your account at http://secure-bank.bad/login",
        "It is very important. I will send you a gift card if you help."
    ]

    for msg in messages:
        print(f"\n[Scammer]: {msg}")
        
        try:
            response = requests.post(
                API_URL, 
                json={"session_id": session_id, "message": msg}, 
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                print(f"[System Status]: {data['status']}")
                print(f"[Arthur]: {data['response']}")
                print(f"[Intelligence]: {data['intelligence']}")
                
                if data['status'] == "Blocked (Known Threat)":
                    print("!!! Scammer Blocked by Cache !!!")
                    break
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print(f"Connection Error: {e}")
            break
        
        time.sleep(1) 


if __name__ == "__main__":
    simulate_scam()
