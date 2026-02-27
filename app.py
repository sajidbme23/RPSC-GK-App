import streamlit as st
import google.generativeai as genai

# Tablet/Mobile Responsive Page Config
st.set_page_config(page_title="RPSC Grade 2 GK", layout="wide")

# Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #1a73e8; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# API Key Access from Secrets (Hide karne ke liye)
try:
    # Streamlit Cloud ke 'Secrets' se key uthayega
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ API Key nahi mili! Kripya Streamlit Settings mein 'Secrets' check karein.")
    st.stop()

# Syllabus Data
syllabus = {
    "🌍 Rajasthan Ka Bhugol": ["Physical features", "Climate & Drainage", "Natural Vegetation", "Agriculture & Livestock", "Demographic Characteristics", "Tourism"],
    "🏰 Itihas aur Sanskriti": ["Ancient Civilizations", "Rajput Dynasties", "1857 Revolution", "Prajamandal Movements", "Lok Devta & Saints", "Fairs & Festivals"],
    "⚖️ Administrative System": ["Governor & CM", "State Legislative Assembly", "High Court", "Panchayati Raj", "RPSC & Lokayukta"],
    "🇮🇳 World & India GK": ["Continents & Oceans", "Global Wind System", "India: Physical & Climate", "Indian Economy", "Foreign Trade"],
    "📜 Constitution & Foreign Policy": ["Constituent Assembly", "Fundamental Rights & Duties", "President & PM", "Parliament", "India's Foreign Policy"],
    "🧠 Educational Psychology": ["Nature & Scope", "Learning Theories", "Personality & Intelligence", "Motivation"]
}

st.title("📖 RPSC 2nd Grade GK Expert")
st.write("Special Test Series for Paper 1")

# Layout
cols = st.columns(2)
for i, (main_topic, subs) in enumerate(syllabus.items()):
    with cols[i % 2]:
        with st.expander(main_topic):
            for sub in subs:
                if st.button(f"Test: {sub}", key=sub):
                    st.session_state.current_sub = sub
                    st.session_state.test_active = True

if st.session_state.get("test_active"):
    st.divider()
    topic = st.session_state.current_sub
    st.header(f"📝 Topic: {topic}")
    
    prompt = f"RPSC 2nd Grade exam ke liye '{topic}' par 5 MCQ sawal Hindi mein banaiye. Har sawal ke 5 options (A-E) dein. Sahi jawab aur detailed Hindi explanation bhi dein."
    
    with st.spinner("Sawal taiyar ho rahe hain..."):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    
    if st.button("⬅️ Wapas Jayein"):
        st.session_state.test_active = False
        st.rerun()
