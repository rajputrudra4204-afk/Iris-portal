# auth.py - Passcodes aur API Keys Config
VIP_PASSCODE = "VIP2919"
OWNER_PASSCODE = "pass@Owner02"

# Yahan apni Google Gemini API Key paste karein
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

def validate_login(role, entered_code):
    if role == "Guest User":
        return True
    elif role == "VIP Member" and entered_code == VIP_PASSCODE:
        return True
    elif role == "System Owner" and entered_code == OWNER_PASSCODE:
        return True
    return False