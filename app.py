import streamlit as st
import google.generativeai as genai

# Page Configuration for Tablet/Mobile
st.set_page_config(page_title="RPSC Grade 2 AI Guru", layout="wide")

# Styling: Buttons ko Tablet par bada aur saaf dikhane ke liye
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 15px; height: 4em; background-color: #0d47a1; color: white; font-size: 18px; font-weight: bold; border: 2px solid #ffca28; margin-bottom: 12px; }
    .stButton>button:hover { background-color: #1565c0; color: #ffca28; }
    .stExpander { border: 2px solid #0d47a1; border-radius: 15px; background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# API Setup (Tier 1 Pro Model)
try:
    # Streamlit Secrets se API key uthayega
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # Aapka pasandida Pro model
    model = genai.GenerativeModel('models/gemini-1.5-pro')
except Exception as e:
    st.error("⚠️ API Key Error: Please check your Streamlit Secrets.")
    st.stop()

# Syllabus Categories from PDF
syllabus = {
    "🌍 Rajasthan: Geography": ["Physical features", "Climate & Drainage", "Natural Vegetation", "Agriculture & Livestock", "Demographic Characteristics", "Industries & Tourism"],
    "🏰 Rajasthan: History": ["Ancient Culture & Civilizations", "Rajput Dynasties & Delhi Sultanate", "Mewar-Mughal Relations", "Freedom Struggle & 1857 Revolution", "Prajamandal & Tribal Movements", "Integration of Rajasthan"],
    "🎭 Art & Culture": ["Lok Devta & Saints", "Architecture (Forts, Temples, Palaces)", "Paintings & Handicrafts", "Fairs & Festivals", "Customs, Dresses & Ornaments", "Folk Music & Dance"],
    "⚖️ Polity & Administration": ["Governor, CM & Council of Ministers", "State Legislative Assembly", "High Court & Subordinate Courts", "Panchayati Raj System", "RPSC & Other Commissions"],
    "🇮🇳 World & India GK": ["Continents & Oceans", "Global Wind System", "India: Physical features & Climate", "Indian Economy: Agri, Industry, Service", "Foreign Trade & Constitution Development"],
    "🧠 Educational Psychology": ["Nature, Scope & Implications", "Holistic Development of Learner", "Learning Theories & Personality", "Intelligence & Creativity", "Motivation & Individual Differences"]
}

st.title("🎓 RPSC 2nd Grade Master (Paper-1)")
st.caption("Tier 1 Active: Gemini 1.5 Pro Assistant")

# Main Interface: Syllabus Buttons
if not st.session_state.get("test_active"):
    st.write("### 📖 Taiyari ke liye Topic Chunein:")
    cols = st.columns(2)
    for i, (main_topic, subs) in enumerate(syllabus.items()):
        with cols[i % 2]:
            with st.expander(main_topic):
                for sub in subs:
                    if st.button(f"Start Test: {sub}", key=sub):
                        st.session_state.current_sub = sub
                        st.session_state.test_active = True
                        st.rerun()

# Test Section with Pro Model Logic
if st.session_state.get("test_active"):
    topic = st.session_state.current_sub
    st.header(f"📝 Test Series: {topic}")
    
    # Powerful Prompt for Pro Model
    prompt = f"""
    Aap ek RPSC (Rajasthan Public Service Commission) ke Senior Teacher exam expert hain. 
    Topic: '{topic}' par 5 sabse mahatvapurn (most important) sawal banaiye.
    
    Niyam (Strict Rules):
    1. Language: Sab kuch HINDI mein hona chahiye.
    2. Format: 5 options dein (A, B, C, D, E). Option E hamesha 'Anuttarit Prashna (अनुत्तरित प्रश्न)' rakhein.
    3. PYQ: Agar ye sawal pichle RPSC Grade 2 exams mein aaya hai, toh saal aur exam ka naam zaroor likhein.
    4. Explanation: Har sawal ke baad uska sahi jawab aur kam se kam 4-5 line ki detail HINDI explanation dein.
    5. Scoring: User ko batayein ki sahi jawab par +2 aur galat par -0.66 (1/3) negative marking hai.
    """
    
    with st.spinner("Gemini Pro aapke liye sawal taiyar kar raha hai..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.button("⬅️ Back to Syllabus"):
        st.session_state.test_active = False
        st.rerun()
