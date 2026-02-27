import streamlit as st
import google.generativeai as genai

# Page Config for Tablet & Mobile
st.set_page_config(page_title="RPSC Grade 2 GK Master", layout="wide")

# Custom CSS for big, easy-to-tap buttons
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #004d40; color: white; width: 100%; border-radius: 8px; height: 3.5em; font-size: 18px; margin-bottom: 10px;
    }
    div.stButton > button:hover { background-color: #00695c; border: 2px solid #ffca28; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
st.sidebar.title("🔑 Admin Setup")
api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# SYLLABUS DATA (From Uploaded PDF)
syllabus = {
    "🌍 Rajasthan Ka Bhugol": ["Physical features", "Climate & Drainage", "Natural Vegetation", "Agriculture & Livestock", "Demographic Characteristics", "Tourism"],
    "🏰 Rajasthan Itihas & Culture": ["Ancient Civilizations", "Rajput Dynasties", "Mewar-Mughal Relations", "1857 Revolution", "Prajamandal & Tribal Movements", "Lok Devta & Saints", "Architecture & Paintings", "Fairs & Festivals"],
    "⚖️ Administrative System": ["Governor & CM", "State Legislative Assembly", "High Court", "Panchayati Raj", "RPSC & Lokayukta"],
    "🇮🇳 World & India GK": ["Continents & Oceans", "Global Wind System", "India: Physical & Climate", "Indian Economy", "Foreign Trade"],
    "📜 Constitution & Foreign Policy": ["Constituent Assembly", "Fundamental Rights & Duties", "President & PM", "Parliament", "India's Foreign Policy"],
    "🧠 Educational Psychology": ["Nature & Scope", "Holistic Development", "Learning Theories", "Personality & Intelligence", "Motivation"]
}

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("📖 RPSC 2nd Grade Paper-1 Taiyari")
    st.info("Topic select karein aur 5-options wali test series shuru karein (Negative Marking ke saath).")

    # Layout for Buttons
    cols = st.columns(2)
    for i, (main_topic, sub_topics) in enumerate(syllabus.items()):
        with cols[i % 2]:
            with st.expander(f"▶️ {main_topic}", expanded=False):
                for sub in sub_topics:
                    if st.button(f"Test: {sub}", key=sub):
                        st.session_state.current_topic = sub
                        st.session_state.test_started = True

    # Test Interface
    if "test_started" in st.session_state and st.session_state.test_started:
        st.divider()
        topic = st.session_state.current_topic
        st.header(f"📝 Mock Test: {topic}")
        
        # Instruction for Gemini
        prompt = f"""
        Aap ek RPSC Senior Teacher (Grade 2) ke expert examiner hain. 
        Topic: '{topic}' par 5 kathin (difficult) sawal banaiye.
        RULES:
        1. Sabhi sawal HINDI mein hone chahiye.
        2. Har sawal ke 5 options (A, B, C, D, E) dein. Option E 'Anuttarit Prashna' rakhein.
        3. Pichle saalon (PYQ) ke RPSC papers ka pattern follow karein.
        4. Har sawal ke baad uska sahi Jawab aur bahut DETAIL mein HINDI EXPLANATION dein.
        5. Agar is topic se pichli exams mein koi sawal aaya hai, toh use 'Previous Year Question' label ke saath zaroor shamil karein.
        """
        
        with st.spinner(f"{topic} ke sawal taiyar ho rahe hain..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.warning("Negative marking (1/3) ka dhyan rakhein!")
            except Exception as e:
                st.error("API Error: Check your key or connection.")

        if st.button("⬅️ Back to Syllabus"):
            st.session_state.test_started = False
            st.rerun()
else:
    st.warning("Pehle sidebar mein apni API key daalein.")
