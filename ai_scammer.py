import requests
import os
import time
import json
import random
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    load_dotenv("backend/.env")

API_KEY = os.getenv("GROQ_API_KEY")
API_SECRET = os.getenv("API_SECRET_KEY", "team_secret_123")
BACKEND_URL = "http://127.0.0.1:8000/chat"

# Initialize Groq Client
client = groq.Groq(api_key=API_KEY)

# Threat Categories Configuration
THREAT_VECTORS = [
    "Romance Fraud (Social Engineering)",
    "Family Emergency Impersonation",
    "Government Agency Impersonation (IRS/Tax)",
    "Cryptocurrency Investment Scheme",
    "Technical Support Fraud",
    "Executive Impersonation (CEO Fraud)"
]

def generate_threat_actor_profile():
    """
    Generates a dynamic threat actor profile using the LLM.
    Returns a dictionary containing the actor's persona, style, and objectives.
    """
    vector = random.choice(THREAT_VECTORS)
    
    system_prompt = f"""
    Task: Generate a realistic profile for a threat actor conducting a '{vector}' campaign.
    
    Output JSON ONLY with the following schema:
    - name: (Pseudonym)
    - origin: (suspected origin)
    - style: (e.g., Aggressive, Manipulative, Professional, Desperate)
    - catchphrase: (Recurring linguistic pattern)
    - asset: (The malicious link, phone number, or wallet address)
    - opening_line: (Initial message to target)
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": system_prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception:
        # Fallback profile in case of generation failure
        return {
            "name": "Unknown_Actor",
            "style": "Generic_Aggressive",
            "asset": "http://malicious-domain.test/verify",
            "opening_line": "Urgent attention required. Verify your account immediately."
        }

def generate_adversarial_response(history_log: str, actor_profile: dict) -> str:
    """
    Generates the next adversarial message based on the conversation history
    and the specific actor profile.
    """
    system_prompt = f"""
    ROLE: You are simulating a threat actor named '{actor_profile['name']}'.
    CAMPAIGN: {actor_profile.get('scam_type', 'General Fraud')}
    BEHAVIORAL PROFILE: {actor_profile['style']}
    OBJECTIVE: Coerce the target into accessing: {actor_profile['asset']}
    
    INSTRUCTIONS:
    1. Maintain strict character adherence.
    2. React realistically to resistance (e.g., frustration, urgency, guilt-tripping).
    3. Keep responses concise (similar to chat protocols).
    4. Do not disclose that this is a simulation.
    """

    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Conversation Log:\n{history_log}\n\nNext Message:"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9
        )
        return completion.choices[0].message.content
    except Exception:
        return "[Connection Error]"

def execute_simulation():
    """
    Main execution loop for the adversarial simulation.
    """
    actor = generate_threat_actor_profile()

    session_id = f"sim_{int(time.time())}"
    current_message = actor['opening_line']
    conversation_log = f"Attacker: {current_message}"
    headers = {"x-api-key": API_SECRET}

    # Execute simulation sequence (10 iterations)
    for turn in range(1, 11):
        print(f"\n[TURN {turn}] Scammer : \n   Message: \"{current_message}\"")
        
        try:
            # Transmit payload to defense system
            payload = {"session_id": session_id, "message": current_message}
            response = requests.post(BACKEND_URL, json=payload, headers=headers)
            
            if response.status_code != 200:
                print(f"[ERROR] API returned status code {response.status_code}")
                break

            data = response.json()
            defense_reply = data.get("response", "...")
            
            print(f"Response :\n   Message: \"{defense_reply}\"")

            # Update conversation context
            conversation_log += f"\nTarget: {defense_reply}"

            current_message = generate_adversarial_response(conversation_log, actor)
            conversation_log += f"\nAttacker: {current_message}"
            
            time.sleep(1.5)

        except KeyboardInterrupt:
            print("\n[INFO] Simulation manually terminated.")
            break
        except Exception as e:
            print(f"[CRITICAL] Simulation Error: {e}")
            break

if __name__ == "__main__":
    execute_simulation()