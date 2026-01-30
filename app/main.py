"""
Main Entry point for the Agentic Honeypot API.
"""
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import custom modules
from app import utils, memory, security, agent

# Load environment variables
load_dotenv()
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

app = FastAPI(title="Agentic Honeypot API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Logs
DASHBOARD_LOGS = []


@app.on_event("startup")
def startup_event():
    """Initialize the database on startup."""
    memory.init_db()


class ChatRequest(BaseModel):
    """Schema for chat requests."""
    session_id: str
    message: str


def verify_api_key(x_api_key: str = Security(APIKeyHeader(name="x-api-key", auto_error=False))):
    """Validate the API key from headers."""
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key


@app.get("/dashboard-data")
def get_dashboard_data():
    """Returns the live logs for the frontend polling."""
    return DASHBOARD_LOGS


@app.post("/chat")
async def chat_endpoint(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """
    Main chat endpoint handling:
    1. Intelligence Extraction
    2. Threat Detection (Session, Database, AI)
    3. Engagement Strategy
    4. Logging
    """
    session_id = request.session_id
    message = request.message
    
    # 1. Intelligence Extraction
    intelligence = utils.extract_intelligence(message)
    
    # 2. Threat Detection
    domains = [
        utils.get_domain(url) 
        for url in intelligence.get("urls", []) 
        if utils.get_domain(url)
    ]
    emails = intelligence.get("emails", [])
    phones = intelligence.get("phone_numbers", [])
    
    threat_detected = False
    threat_source = "clean"
    confidence = 0.0

    # A. Check Ongoing Session
    existing_session = memory.get_session(session_id)
    if existing_session:
        threat_detected = True
        threat_source = "ongoing_session"

    # B. Check Cache (Database)
    if not threat_detected:
        # Check Domains
        for domain in domains:
            if memory.check_cache(domain):
                threat_detected = True
                threat_source = "known_database"
                break
        # Check Emails
        if not threat_detected:
            for email in emails:
                if memory.check_cache(email):
                    threat_detected = True
                    threat_source = "known_database"
                    break

    # C. Check AI Guard
    if not threat_detected:
        is_scam, score = security.predict_scam(message)
        if is_scam:
            threat_detected = True
            threat_source = "ai_guard"
            confidence = score
            
            # Save all entities to database
            for domain in domains:
                memory.update_cache(domain, "SCAM_URL", confidence)
            for email in emails:
                memory.update_cache(email, "SCAM_EMAIL", confidence)
            for phone in phones:
                memory.update_cache(phone, "SCAM_PHONE", confidence)

    # 3. Engagement
    if threat_detected:
        bot_reply = agent.generate_reply(session_id, message)
        response_data = {
            "response": bot_reply,
            "intelligence": intelligence,
            "status": "engaged",
            "source": threat_source
        }
    else:
        response_data = {
            "response": "Message received (Safe).",
            "intelligence": intelligence,
            "status": "ignored"
        }

    # 4. Logging
    if threat_detected:
        log_entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "session_id": session_id,
            "scammer_msg": message,
            "bot_response": response_data["response"],
            "intelligence": intelligence,
            "threat_source": threat_source
        }
        DASHBOARD_LOGS.insert(0, log_entry)
        if len(DASHBOARD_LOGS) > 50:
            DASHBOARD_LOGS.pop()

    return response_data


@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "running"}