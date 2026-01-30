"""
Security module for threat detection using machine learning or heuristics.
"""
import os
from typing import Tuple

# Placeholder for model path
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml_assets",
    "scam_model"
)


class SecurityGuard:
    """Handles logic for detecting scam attempts."""

    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Attempt to load a local BERT model."""
        if os.path.exists(MODEL_PATH):
            try:
                # Placeholder for loading actual model
                # self.model = pipeline("text-classification", model=MODEL_PATH)
                print(f"Model loaded from {MODEL_PATH}")
            except Exception as e:
                print(f"Failed to load model: {e}")
                self.model = None
        else:
            print("No local model found. Using keyword fallback.")
            self.model = None

    def predict_scam(self, text: str) -> Tuple[bool, float]:
        """
        Predict if the text is a scam.

        Args:
            text (str): The input text to analyze.

        Returns:
            Tuple[bool, float]: (is_scam, confidence_score)
        """
        if self.model:
            # Placeholder for actual model inference
            return False, 0.0
        else:
            return self._keyword_fallback(text)

    def _keyword_fallback(self, text: str) -> Tuple[bool, float]:
        """Simple keyword-based detection."""
        text_lower = text.lower()
        scam_keywords = [
            "urgent", "verify your account", "bank", "password", 
            "credit card", "social security", "immediately", 
            "suspended", "winner", "lottery", "prize", "wire transfer",
            "gift card", "refund"
        ]
        
        match_count = sum(1 for keyword in scam_keywords if keyword in text_lower)
        
        if match_count > 0:
            confidence = min(0.5 + (match_count * 0.1), 0.99)
            return True, confidence
        
        return False, 0.0


# Singleton instance
guard = SecurityGuard()


def predict_scam(text: str) -> Tuple[bool, float]:
    """Helper function to access the singleton guard instance."""
    return guard.predict_scam(text)
