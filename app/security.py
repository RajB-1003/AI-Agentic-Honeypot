import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# 1. Define Paths
# Uses relative path so it works on any computer
local_model_path = os.path.join(os.path.dirname(__file__), "../ml_assets/scam_model")

# CHANGE THIS LINE TO YOUR NEW ID:
cloud_model_name = "RajB1003/honey-pot-guard" 

# 2. Smart Loader
def load_security_model():    
    # CHECK: Does the local folder exist?
    if os.path.exists(local_model_path) and os.listdir(local_model_path):
        print(f"Found local model at: {local_model_path}")
        return (
            AutoTokenizer.from_pretrained(local_model_path),
            AutoModelForSequenceClassification.from_pretrained(local_model_path)
        )
    else:
        # This now downloads YOUR specific model, not the generic one
        print(f"Local model not found. Downloading {cloud_model_name}")
        return (
            AutoTokenizer.from_pretrained(cloud_model_name),
            AutoModelForSequenceClassification.from_pretrained(cloud_model_name)
        )

# 3. Initialize
tokenizer, model = load_security_model()