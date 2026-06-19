# auth.py - Security Codes aur API Keys
VIP_PASSCODE = "VIP123"
OWNER_PASSCODE = "OWNER7788"

# ⚠️ Yahan apni Google Gemini API Key paste karein [3]
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

def validate_login(role, entered_code):
    if role == "Guest User":
        return True
    elif role == "VIP Study Partner" and entered_code == VIP_PASSCODE:
        return True
    elif role == "System Owner" and entered_code == OWNER_PASSCODE:
        return True
    return False