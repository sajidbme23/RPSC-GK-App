import streamlit as st
import google.generativeai as genai
import time

# --- 1. PAGE CONFIG (Tablet/Mobile Friendly) ---
st.set_page_config(
    page_title="RPSC 2nd Grade AI Guru",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="📖"
)

# Custom Styling (Buttons ko bada aur clean dikhane ke liye)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.8em; background-color: #0d47a1; color: white; font-weight: bold; border: 2px solid #ffca28; }
    .stExpander { border: 2px solid #0d47a1; border-radius: 12px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE API CONFIGURATION ---
try:
    # Aapki PDI app ki tarah 'GEMINI_API_KEY' use kar raha hoon
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ API Key nahi mili! Settings > Secrets mein GEMINI_API_KEY set karein.")
    st.stop()

# --- 3. SYLLABUS DATA (From Your PDF) ---
syllabus = {
    "🌍 Rajasthan: Geography": ["Physical features", "Climate & Drainage", "Natural Vegetation", "Agriculture & Livestock", "Demographic Characteristics", "Tourism centres"],
    "🏰 Rajasthan: History": ["Ancient Civilizations", "Rajput Dynasties", "Mewar-Mughal Relations", "1857 Revolution", "Prajamandal & Tribal Movements", "Integration of Rajasthan"],
    "🎭 Art & Culture": ["Lok Devta & Saints", "Architecture (Forts & Temples)", "Paintings & Fairs", "Customs, Dresses & Ornaments", "Folk Music & Dance"],
    "⚖️ Polity & Admin": ["Governor, CM & Council of Ministers", "State Legislative Assembly", "High Court", "Panchayati Raj System", "RPSC & Commissions"],
    "🇮🇳 World & India GK": ["Continents & Oceans", "Global Wind System", "India: Physical & Climate", "Indian Economy", "Foreign Trade"],
    "📜 Constitution": ["Constituent Assembly", "Fundamental Rights & Duties", "President & PM", "Parliament", "India's Foreign Policy"],
    "🧠 Educational Psychology": ["Nature & Scope", "Learner Development", "Learning Theories", "Personality & Intelligence", "Motivation"]
}

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/education.png", width=80)
    st.title("Study Control Center")
    st.info("Tier 1 Active: Gemini 3.1 Pro")
    st.markdown("---")
    if st.button("Clear History"):
        st.session_state.test_active = False
        st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title("📖 RPSC 2nd Grade Paper-1 Expert")
st.caption("Special Test Series for Biwi's Preparation")

if not st.session_state.get("test_active"):
    st.subheader("📚 Syllabus Topics")
    cols = st.columns(2)
    for i, (main_topic, subs) in enumerate(syllabus.items()):
        with cols[i % 2]:
            with st.expander(main_topic):
                for sub in subs:
                    if st.button(f"Start: {sub}", key=sub):
                        st.session_state.current_sub = sub
                        st.session_state.test_active = True
                        st.rerun()

# --- 6. TEST GENERATION (Gemini 3.1 Pro) ---
if st.session_state.get("test_active"):
    topic = st.session_state.current_sub
    st.header(f"📝 Topic: {topic}")
    
    # Using the same Pro model as your PDI app
    model = genai.GenerativeModel("gemini-3.1-pro-preview")
    
    prompt = f"""
    Aap ek RPSC (Rajasthan Public Service Commission) ke Senior Teacher exam expert hain. 
    Syllabus Topic: '{topic}' par 5 sabse mahatvapurn (most important) sawal banaiye.
    
    Rules:
    1. Poora content HINDI mein hona chahiye.
    2. Format: 5 options (A, B, C, D, E). Option E: 'Anuttarit Prashna'.
    3. PYQ: Agar ye pichle RPSC exams mein aaya hai, toh mention karein.
    4. Explanation: Har sawal ke baad detail mein Hindi explanation dein.
    5. Scoring: +2 for correct, -0.66 for wrong.
    """
    
    with st.spinner(f"Gemini 3.1 Pro analysis kar raha hai..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.button("⬅️ Wapas Syllabus par Jayein"):
        st.session_state.test_active = False
        st.rerun()
