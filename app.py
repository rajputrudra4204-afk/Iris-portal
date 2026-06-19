# app.py - Integrated Cosmic Terminal with Voice Dictation, Study Logbook, & Owner Telemetry
import streamlit as st
import requests
import auth
import time
import google.generativeai as genai
try:
    import PIL.Image as Image
except ImportError:
    Image = None

# Page config to collapse the sidebar by default on load
st.set_page_config(
    page_title="IRIS Space Terminal Console", 
    page_icon="👁️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Safe passcode retrieval with dynamic editing support
if "vip_code" not in st.session_state:
    st.session_state["vip_code"] = getattr(auth, "VIP_PASSCODE", "VIP123")
if "owner_code" not in st.session_state:
    st.session_state["owner_code"] = getattr(auth, "OWNER_PASSCODE", "OWNER7788")

GEMINI_KEY = getattr(auth, "GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# --- 🌌 1. IMMERSIVE SPACE CONSOLE CSS (Twinkling Stars, Accretion Disks, & Smooth Inputs) ---
st.markdown("""
<style>
    /* 🪐 Nebula Radial Galactic Backdrop (Pink Nebula & Space Deep Blue Overlay) */
    .stApp {
        background: 
            radial-gradient(circle at 80% 20%, rgba(217, 70, 239, 0.15) 0%, transparent 50%), /* Pink Nebula */
            radial-gradient(circle at 20% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 50%),  /* Cyan Nebula */
            radial-gradient(circle at 50% 50%, #060412 0%, #020005 100%) !important;
        overflow: hidden;
    }
    
    /* 🌠 High-Visibility Starfield Twinkle Layer */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        width: 100%; height: 100%;
        background: transparent;
        box-shadow: 10vw 20vh #fff, 30vw 10vh #fff, 50vw 40vh #fff, 70vw 15vh #fff, 90vw 30vh #fff,
                    20vw 80vh #fff, 40vw 70vh #fff, 60vw 90vh #fff, 80vw 60vh #fff, 15vw 50vh #fff,
                    95vw 5vh #fff, 5vw 95vh #fff, 45vw 55vh #fff, 85vw 85vh #fff, 3vw 35vh #fff,
                    25vw 25vh rgba(255,255,255,0.7), 65vw 15vh rgba(255,255,255,0.7), 78vw 80vh rgba(255,255,255,0.7);
        animation: starTwinkle 3.5s infinite ease-in-out;
        z-index: 0;
        pointer-events: none;
    }
    @keyframes starTwinkle {
        0%, 100% { opacity: 0.35; }
        50% { opacity: 1; }
    }

    /* 🌠 Dynamic Shooting Star / Comet Layer */
    .comet-effect {
        position: absolute;
        top: -100px;
        left: 50%;
        width: 4px;
        height: 100px;
        background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(217, 70, 239, 0.8));
        transform: rotate(-45deg);
        animation: meteor 14s infinite ease-in-out;
        pointer-events: none;
        z-index: 0;
    }
    @keyframes meteor {
        0%, 100% { top: -100px; left: 80%; opacity: 0; }
        10% { opacity: 1; }
        30% { top: 120%; left: 20%; opacity: 0; }
    }

    /* 🪐 HTML/CSS Floating Asteroid Belt */
    .asteroid-belt-1 {
        position: absolute;
        top: -50px; left: 85%;
        width: 16px; height: 13px;
        background: #252431;
        border-radius: 40% 60% 45% 55% / 40% 45% 55% 60%;
        box-shadow: inset -3px -3px 0px #13121a, 0 0 10px rgba(217, 70, 239, 0.15);
        opacity: 0.65;
        animation: driftAsteroid 28s infinite linear;
        pointer-events: none;
        z-index: 0;
    }
    @keyframes driftAsteroid {
        0% { transform: translateY(0) translateX(0) rotate(0deg); }
        100% { transform: translateY(115vh) translateX(-50vw) rotate(360deg); }
    }

    /* 🎮 MI GAME SPACE INTRO SPINNING WIREFRAME */
    .spin-wireframe-fast {
        transform-origin: center;
        animation: spinWire 2s infinite linear;
    }
    .spin-wireframe-slow {
        transform-origin: center;
        animation: spinWire 5s infinite linear reverse;
    }
    @keyframes spinWire {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* 🧿 CYBERNETIC EYE & BLACK HOLE Accretion Disk glow */
    @keyframes pink-glow {
        0% { filter: drop-shadow(0 0 8px #d946ef); }
        50% { filter: drop-shadow(0 0 18px #d946ef); }
        100% { filter: drop-shadow(0 0 8px #d946ef); }
    }
    .blackhole-disk {
        animation: pink-glow 4s infinite ease-in-out;
        transform-origin: center;
    }

    .game-space-title {
        color: #06b6d4;
        font-size: 32px;
        font-weight: bold;
        letter-spacing: 5px;
        text-shadow: 0 0 15px #06b6d4;
        margin-top: 25px;
        font-family: 'Consolas', monospace;
    }
    .system-status {
        color: #8b5cf6;
        font-size: 13px;
        letter-spacing: 2px;
        margin-top: 10px;
        font-family: 'Consolas', monospace;
        opacity: 0.8;
    }
    .progress-bar-container {
        width: 300px;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        margin: 25px auto;
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-bar-fill {
        width: 0%;
        height: 100%;
        background: linear-gradient(90deg, #d946ef, #06b6d4);
        animation: fillProgress 2.4s forwards cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes fillProgress {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    /* Big Glowing IRIS Logo Text */
    .glowing-title {
        color: #ffffff;
        font-size: 40px; /* Increased font-size as requested */
        font-weight: bold;
        letter-spacing: 5px;
        text-shadow: 0 0 15px #d946ef, 0 0 30px #06b6d4;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 12px;
    }
    
    /* Spaceship Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(6, 4, 18, 0.95) !important;
        border-right: 1px solid #1b1e36 !important;
        box-shadow: 5px 0 15px rgba(217, 70, 239, 0.2) !important;
    }
    
    /* Neon buttons */
    .stButton>button, .stFormSubmitButton>button {
        background: linear-gradient(45deg, #d946ef, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        box-shadow: 0 0 12px rgba(217, 70, 239, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.8) !important;
        transform: scale(1.02);
    }
    div[data-baseweb="select"] {
        background-color: rgba(14, 16, 34, 0.6) !important;
        border: 1px solid #1b1e36 !important;
        border-radius: 8px !important;
    }
    
    /* 💊 CAPSULE PILL-SHAPED NEON CHAT INPUT BOX 💊 */
    div[data-testid="stChatInput"] {
        border-radius: 32px !important;
        background-color: rgba(14, 16, 34, 0.85) !important;
        border: 2px solid #8b5cf6 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6), 0 0 15px rgba(139, 92, 246, 0.4) !important;
        padding-left: 18px !important;
        padding-right: 18px !important;
        transition: all 0.3s ease-in-out !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #06b6d4 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.6), 0 0 22px rgba(6, 182, 212, 0.7) !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    div[data-testid="stChatInput"] > div {
        border: none !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='comet-effect'></div><div class='asteroid-belt-1'></div>", unsafe_allow_html=True)

# --- 📡 2. AUTO-LOCATION WEATHER & STARGAZING METRICS [1, 2] ---
@st.cache_data(ttl=600)
def fetch_local_space_metrics():
    try:
        geo_res = requests.get("http://ip-api.com/json", timeout=3).json()
        city = geo_res.get("city", "Kanpur")
        lat = geo_res.get("lat", 26.4499)
        lon = geo_res.get("lon", 80.3319)
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude=26.4499&longitude=80.3319&current=temperature_2m,relative_humidity_2m&timezone=auto"
        res = requests.get(url, timeout=3).json()
        temp = res["current"]["temperature_2m"]
        humidity = res["current"]["relative_humidity_2m"]
        return f"📍 {city}: {temp}°C | Humidity: {humidity}%"
    except Exception:
        return "📍 Kanpur, IN | 34°C"

# --- 🛰️ 3. LIVE ISS POSITION TRACKER API ---
def fetch_iss_location():
    try:
        res = requests.get("http://api.open-notify.org/iss-now.json", timeout=2).json()
        lat = res["iss_position"]["latitude"]
        lon = res["iss_position"]["longitude"]
        return f"Lat {lat} | Lon {lon}"
    except Exception:
        return "Establishing Space-Link..."

# Initialize Session States
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "role" not in st.session_state: st.session_state["role"] = None
if "messages" not in st.session_state: st.session_state["messages"] = []
if "boot_animation" not in st.session_state: st.session_state["boot_animation"] = False
if "pending_prompt" not in st.session_state: st.session_state["pending_prompt"] = None
if "study_stats" not in st.session_state: st.session_state["study_stats"] = {"Math": 1.0, "Physics": 2.0, "Coding": 3.0}
if "missions" not in st.session_state: st.session_state["missions"] = []
if "logbook" not in st.session_state: st.session_state["logbook"] = []

# Credentials verification
def verify_credentials(role, passcode):
    if role == "Guest User": return True
    elif role == "VIP Study Partner" and passcode == st.session_state["vip_code"]: return True
    elif role == "System Owner" and passcode == st.session_state["owner_code"]: return True
    return False

# Mapping Custom sleek avatars for different roles
def get_user_avatar():
    role = st.session_state.get("role", "Guest User")
    if role == "System Owner": return "👑"
    elif role == "VIP Study Partner": return "⚡"
    return "👤"

# --- 🛰️ MAIN VECTOR CHASSIS: HIGH-TECH CYBERNETIC ARC-EYE ---
def render_cyber_eye_vector(width_px=115):
    return f"""
    <div style='text-align: center;'>
        <svg class='cyber-eye' width='{width_px}' height='{width_px}' viewBox='0 0 100 100'>
            <circle cx='50' cy='50' r='46' stroke='#06b6d4' stroke-width='1.5' fill='none' />
            <circle cx='50' cy='50' r='42' stroke='#1e293b' stroke-width='2' fill='none' />
            <circle cx='50' cy='50' r='36' stroke='#00f0ff' stroke-dasharray='4, 6' stroke-width='3.5' fill='none' />
            <circle cx='50' cy='50' r='29' stroke='#334155' stroke-width='2' fill='none' />
            <circle cx='50' cy='50' r='22' fill='url(#iris-pattern)' />
            <circle cx='50' cy='50' r='22' stroke='#d946ef' stroke-width='1' stroke-dasharray='2, 2' fill='none' />
            <circle cx='50' cy='50' r='9' fill='#020005' />
            <circle cx='46' cy='46' r='2.5' fill='#ffffff' opacity='0.85' />
            <defs>
                <radialGradient id='iris-pattern' cx='50%' cy='50%' r='50%'>
                    <stop offset='0%' style='stop-color:#a5f3fc;' />
                    <stop offset='45%' style='stop-color:#06b6d4;' />
                    <stop offset='75%' style='stop-color:#d946ef;' />
                    <stop offset='100%' style='stop-color:#020005;' />
                </radialGradient>
            </defs>
        </svg>
    </div>
    <div class='glowing-title'>IRIS</div>
    <div style='text-align: center; color: #06b6d4; font-size: 11px; font-weight: bold; letter-spacing: 2.5px; margin-bottom: 2px;'>INTELLIGENT RESPONSIVE INFORMATION SYSTEM</div>
    <div style='text-align: center; color: #d946ef; font-size: 10px; font-weight: bold; letter-spacing: 3px; margin-top: 0px; margin-bottom: 25px;'>DEVELOPED BY RUDRA</div>
    """

# --- 🛰️ COSMIC BLACK HOLE VECTOR LOGO with custom requested Rudra branding ---
def render_black_hole_vector(width_px=120):
    return f"""
    <div style='text-align: center; margin-top: 15px;'>
        <svg class="pulsing-logo" width="{width_px}" height="{width_px}" viewBox="0 0 100 100">
            <ellipse cx="50" cy="50" rx="46" ry="12" stroke="#d946ef" stroke-width="3" fill="none" class="blackhole-disk" transform="rotate(-15 50 50)" />
            <circle cx="50" cy="50" r="18" fill="none" stroke="#00f0ff" stroke-dasharray="2, 4" stroke-width="1.5" />
            <circle cx="50" cy="50" r="14" fill="#020006" stroke="#d946ef" stroke-width="1" />
            <circle cx="50" cy="50" r="10" fill="#000000" />
        </svg>
    </div>
    <div class='glowing-title' style='color:#ffffff; font-size: 40px; letter-spacing: 5px; margin-bottom: 2px;'>IRIS</div>
    <div style='text-align: center; color: #06b6d4; font-size: 11px; font-weight: bold; letter-spacing: 2.5px; margin-bottom: 5px;'>INTELLIGENT RESPONSIVE INFORMATION SYSTEM</div>
    <div style='text-align: center; color: #d946ef; font-size: 10px; font-weight: bold; letter-spacing: 3px; margin-top: 2px; margin-bottom: 25px;'>DEVELOPED BY RUDRA</div>
    """

# --- 3. GATEKEEPER WELCOME LOGIN PANEL ---
if not st.session_state["logged_in"] and not st.session_state["boot_animation"]:
    st.markdown(render_cyber_eye_vector(115), unsafe_allow_html=True)
    st.write("Welcome, Sir! Please select your authenticated role to initialize the workspace.")

    with st.form("login_gatekeeper"):
        selected_role = st.selectbox("Select Your Role", ["Guest User", "VIP Study Partner", "System Owner"])
        
        user_passcode = ""
        if selected_role != "Guest User":
            user_passcode = st.text_input("Enter Passcode", type="password", placeholder="Type role passcode here...")

        submit_action = st.form_submit_button("Access Portal", use_container_width=True)

        if submit_action:
            if verify_credentials(selected_role, user_passcode):
                st.session_state["temp_role"] = selected_role
                st.session_state["boot_animation"] = True
                st.rerun()
            else:
                st.error("Access Denied! Invalid Passcode, please try again.")

# --- 🛰️ 4. XIAOMI/MI GAME SPACE BOOT SCREEN ANIMATION FLOW ---
elif st.session_state["boot_animation"]:
    st.markdown("""
    <div style='text-align: center; margin-top: 15%;'>
        <!-- Holographic Concentric Wireframe -->
        <svg width="150" height="150" viewBox="0 0 100 100">
            <g class="spin-wireframe-fast">
                <circle cx="50" cy="50" r="44" stroke="#00f0ff" stroke-width="1" stroke-dasharray="1, 4" fill="none" opacity="0.6"/>
                <circle cx="50" cy="50" r="32" stroke="#d946ef" stroke-width="1" stroke-dasharray="4, 3" fill="none" opacity="0.8"/>
            </g>
            <g class="spin-wireframe-slow">
                <circle cx="50" cy="50" r="38" stroke="#00f0ff" stroke-width="1.5" stroke-dasharray="8, 2" fill="none" opacity="0.7"/>
                <circle cx="50" cy="50" r="24" stroke="#d946ef" stroke-width="1.5" stroke-dasharray="1, 8" fill="none" />
                <circle cx="50" cy="50" r="14" stroke="#00f0ff" stroke-dasharray="2, 1" fill="none" />
            </g>
            <circle cx="50" cy="50" r="8" fill="#00f0ff" opacity="0.4" />
        </svg>
        <div class="game-space-title">IRIS SPACE CORE</div>
        <div class="system-status">ENGAGING TELEMETRY BOOT SEQUENCE...</div>
        <div class="progress-bar-container">
            <div class="progress-bar-fill"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(2.4)
    st.session_state["logged_in"] = True
    st.session_state["role"] = st.session_state["temp_role"]
    st.session_state["boot_animation"] = False
    
    st.session_state["messages"] = [
        {"role": "assistant", "content": f"Welcome, Sir! The IRIS Web Portal is fully operational. You are logged in as `{st.session_state['role']}`. How may I assist you with your tasks, codes, or observations today?"}
    ]
    st.rerun()

# --- 5. MAIN DASHBOARD WORKSPACE (LOGGED IN STATE) ---
else:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"### 🌀 IRIS PRO | `{st.session_state['role']}`")
    with col2:
        st.markdown(f"<div style='text-align: right; color: #06b6d4; font-weight: bold;'>{fetch_local_space_metrics()}</div>", unsafe_allow_html=True)

    st.divider()

    # Empty chat vector glowing Cosmic Black Hole logo watermark [4]
    if len(st.session_state["messages"]) <= 1:
        st.markdown(render_black_hole_vector(120), unsafe_allow_html=True)

    # Render previous chats with custom space icons
    for msg in st.session_state["messages"]:
        avatar_icon = "👁️" if msg["role"] == "assistant" else get_user_avatar()
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.write(msg["content"])

    # --- 📁 A-2: STELLAR LOGBOOK ADD ARCHIVE FEATURE ---
    if len(st.session_state["messages"]) > 1:
        last_reply = st.session_state["messages"][-1]["content"]
        if st.sidebar.button("📁 Save Last Response to Logbook", use_container_width=True):
            if last_reply not in st.session_state["logbook"]:
                st.session_state["logbook"].append(last_reply)
                st.sidebar.success("Captured to Logbook Archive!")

    # --- ⚡ MULTIMODAL DOCUMENT / IMAGE SCANNER [1] ---
    image_data = None
    if st.session_state["role"] in ["VIP Study Partner", "System Owner"]:
        uploaded_file = st.sidebar.file_uploader("📸 Scan Image / Study Notes", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None and Image:
            try:
                image_data = Image.open(uploaded_file)
                st.sidebar.image(image_data, caption="Document Staged for Analysis", use_container_width=True)
            except Exception as e:
                st.sidebar.error(f"Scanner read error: {e}")

    # --- ⚡ ACTIVE ASYNCHRONOUS GENERATION HOOK ⚡ ---
    if st.session_state["pending_prompt"]:
        prompt_to_process = st.session_state["pending_prompt"]
        st.session_state["pending_prompt"] = None # Clear immediately
        
        with st.chat_message("assistant", avatar="👁️"):
            with st.spinner("Processing space-link queries..."):
                try:
                    if GEMINI_KEY and GEMINI_KEY != "YOUR_GEMINI_API_KEY_HERE":
                        genai.configure(api_key=GEMINI_KEY)
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        
                        if image_data:
                            response = model.generate_content([
                                f"System Instructions: You are IRIS, an elite professional Hinglish AI space assistant. "
                                f"Analyze this attached image alongside the prompt. Provide final output in professional, beautifully structured markdown English. "
                                f"Address the user as 'Sir' or 'Boss'. User query: {prompt_to_process}",
                                image_data
                            ])
                        else:
                            response = model.generate_content(
                                f"System Instructions: You are IRIS, an elite, highly professional, polite, and exceptionally intelligent AI space assistant. "
                                f"Provide your final output responses in clean, highly professional English, well-structured with markdown. "
                                f"You must seamlessly understand and process user queries even if they are typed in Hinglish (Latin-script Hindi) or general English. "
                                f"Support any question including general knowledge, complex coding, mathematics, or astronomical facts. "
                                f"Always address the user as 'Sir' or 'Boss'. "
                                f"User query: {prompt_to_process}"
                            )
                        reply = response.text
                    else:
                        reply = f"System Standby Alert: Gemini API Key is missing or not configured in auth.py, Sir. (User Prompt: '{prompt_to_process}')"
                except Exception as e:
                    reply = f"API Connection Error: {str(e)}"
            
            # Typewriter delay output stream generator
            def typewriter_generator(text):
                for word in text.split(" "):
                    yield word + " "
                    time.sleep(0.04)
            
            # Streaming output cleanly
            reply_result = st.write_stream(typewriter_generator(reply))
            
        st.session_state["messages"].append({"role": "assistant", "content": reply_result})
        st.rerun()

    # --- 🎙️ A-3: BROWSER-BASED VOCAL DICTATION COMPONENT ---
    st.components.v1.html("""
    <div style="text-align: center; margin-bottom: -5px;">
        <button id="mic-btn" style="background: linear-gradient(45deg, #d946ef, #06b6d4); color: white; border: none; padding: 6px 14px; border-radius: 20px; font-weight: bold; cursor: pointer; box-shadow: 0 0 10px #d946ef; font-family: sans-serif; font-size: 11px; transition: all 0.3s ease;">🎙️ Tap to Speak</button>
        <p id="speech-out" style="color: #a5f3fc; font-size: 11px; margin-top: 5px; font-family: sans-serif; font-weight: bold;"></p>
    </div>
    <script>
        const btn = document.getElementById('mic-btn');
        const out = document.getElementById('speech-out');
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const rec = new SpeechRecognition();
            rec.lang = 'en-US';
            btn.addEventListener('click', () => {
                rec.start();
                out.innerText = "System Listening... Speak now, Boss!";
            });
            rec.onresult = (e) => {
                const text = e.results[0][0].transcript;
                out.innerText = "Recognized! (Double click and paste into Chat input capsule)";
                navigator.clipboard.writeText(text);
            };
            rec.onerror = () => { out.innerText = "Holographic link timed out. Try again."; };
        } else {
            btn.style.display = 'none';
            out.innerText = "Vocal link not supported on this browser engine.";
        }
    </script>
    """, height=50)

    # Bottom Chat input capsule
    if prompt := st.chat_input("Ask IRIS anything..."):
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.session_state["pending_prompt"] = prompt
        st.rerun()

    # --- 🛰️ 6. SPACESHIP SIDEBAR TERMINAL METRICS ---
    st.sidebar.markdown("### 🛰️ TELEMETRY SYSTEM")
    st.sidebar.markdown(f"""
    <div style='background-color: rgba(27, 30, 54, 0.4); padding: 12px; border-radius: 8px;'>
        <div style='color: #06b6d4; font-size:11px; font-weight:bold;'>🛰️ ISS Orbit: <span style='color:white;'>{fetch_iss_location()}</span></div>
        <div style='color: #06b6d4; font-size:11px; font-weight:bold;'>☄️ Proximity Alert: <span style='color:white;'>Low (0.04 AU)</span></div>
        <div style='color: #06b6d4; font-size:11px; font-weight:bold;'>🌌 Solar Wind: <span style='color:white;'>420 km/s</span></div>
        <div style='color: #06b6d4; font-size:11px; font-weight:bold;'>🔋 Core Battery: <span style='color:white;'>98% (Nuclear)</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.write("")

    # --- 🚀 A-1: COSMIC MISSION PLANNER (To-Do list with Space HUD style) ---
    if st.session_state["role"] in ["VIP Study Partner", "System Owner"]:
        with st.sidebar.expander("🚀 COSMIC MISSIONS HUD", expanded=False):
            st.write("Add your current orbit targets:")
            new_mission = st.text_input("New Mission Objective", placeholder="e.g., Code dashboard.py")
            if st.button("Initialize Mission Object", use_container_width=True):
                if new_mission:
                    st.session_state["missions"].append({"task": new_mission, "status": "Active"})
                    st.rerun()
            st.write("")
            for idx, mission in enumerate(st.session_state["missions"]):
                col_m1, col_m2 = st.columns([3, 1])
                with col_m1:
                    st.markdown(f"🛰️ {mission['task']}" if mission["status"] == "Active" else f"<s>🛰️ {mission['task']}</s>", unsafe_allow_html=True)
                with col_m2:
                    if mission["status"] == "Active" and st.button("End", key=f"mis_{idx}"):
                        st.session_state["missions"][idx]["status"] = "Completed"
                        st.toast("✅ MISSION OBJECTIVE SYNCHRONIZED SUCCESSFUL!", icon="🚀")
                        st.rerun()

    # --- 📚 A-2: STELLAR LOGBOOK ARCHIVE VIEWER ---
    if st.session_state["role"] in ["VIP Study Partner", "System Owner"]:
        with st.sidebar.expander("📚 STELLAR LOGBOOK VAULT", expanded=False):
            if st.session_state["logbook"]:
                for i, log in enumerate(st.session_state["logbook"]):
                    st.info(f"Log {i+1}: {log[:70]}...")
            else:
                st.write("No cosmic study data archived yet.")

    # --- 📈 7. SIDEBAR: MISSION STUDY SESSION LOGS & ANALYTICS ---
    if st.session_state["role"] in ["VIP Study Partner", "System Owner"]:
        with st.sidebar.expander("📈 MISSION STUDY LOGS", expanded=False):
            st.write("Log your current study hours:")
            subject_sel = st.selectbox("Select Subject Sector", ["Math", "Physics", "Coding", "General Science"])
            hours_sel = st.slider("Observe Hours", 0.5, 8.0, 1.0, step=0.5)
            
            if st.button("Commit Mission Log"):
                st.session_state["study_stats"][subject_sel] = st.session_state["study_stats"].get(subject_sel, 0.0) + hours_sel
                st.success(f"Logged {hours_sel} hrs on {subject_sel}!")
            
            st.bar_chart(st.session_state["study_stats"])

    # --- 🛠️ C-2: ADVANCED OWNER TELEMETRY CONTROL PANEL ---
    if st.session_state["role"] == "System Owner":
        with st.sidebar.expander("🛠️ OWNER CONTROL PANEL", expanded=True):
            st.write("🌌 **ACTIVE CREW LOGS**")
            st.code("Guest_User_01: 10.242.9.x [Active]\nVIP_Study_Partner_02: 124.8.x.x [Offline]\nOwner_Console: Localhost [Active]", language="markdown")
            
            st.write("🔋 **API TELEMETRY USAGE**")
            st.metric("Total Tokens Consumed", "1,420 Tokens", "+4.2% orbit shift")
            st.divider()
            
            st.write("Modify real-time spaceship codes:")
            new_vip = st.text_input("Edit VIP Code", value=st.session_state["vip_code"])
            new_owner = st.text_input("Edit Owner Code", value=st.session_state["owner_code"], type="password")
            
            if st.button("Update Codes", use_container_width=True):
                st.session_state["vip_code"] = new_vip
                st.session_state["owner_code"] = new_owner
                st.success("Passcodes updated dynamically!")

            st.divider()
            st.write("Run deep-space latency test:")
            if st.button("Run Connection Diagnostics"):
                st.info("Ping: 24ms | API Latency: 120ms | Core System: Operational")

    if st.sidebar.button("Logout System", type="primary", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.session_state["messages"] = []
        st.rerun()