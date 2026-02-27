import streamlit as st
import google.generativeai as genai

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="RPSC 2nd Grade Paper-1 Expert",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="📖"
)

# UI Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 12px; height: 3.8em; background-color: #0b3d91; color: white; font-weight: bold; border: 2px solid #f4c20d; font-size: 15px; }
    .stButton>button:hover { background-color: #0a2e6b; color: #f4c20d; }
    .stExpander { border: 2px solid #0b3d91; border-radius: 12px; background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE API CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ API Key Error: Streamlit Settings > Secrets mein 'GEMINI_API_KEY' set karein.")
    st.stop()

# --- 3. OFFICIAL SYLLABUS DATA ---
syllabus = {
    "🌍 Part I: Rajasthan Geography": ["Physical features, Climate, Drainage", "Natural Vegetation, Agriculture, Livestock", "Demographic Characteristics, Tribes", "Industries, Tourism and Tourist Centres"],
    "🏰 Part I: Rajasthan History": ["Ancient Culture & Civilization", "Rajput Dynasties & Delhi Sultanate", "Mughal Relations (Sanga, Pratap, etc.)", "1857 Revolution", "Prajamandal & Tribal Movements", "Integration of Rajasthan"],
    "🎭 Part I: Rajasthan Culture": ["Lok Devta & Saints", "Architecture (Temples, Forts)", "Paintings, Fairs & Festivals", "Customs, Dresses & Ornaments", "Folk Music, Dance & Literature", "Leading Personalities"],
    "⚖️ Part I: Rajasthan Admin": ["Governor, CM & Assembly", "High Court & Subordinate Courts", "Panchayati Raj & Urban Local Govt", "RPSC, Election & Finance Commissions"],
    "📰 Part II: Current Affairs": ["Important Persons & Places", "New Schemes & Welfare Initiatives", "Sports, Awards, Books & Authors"],
    "🇮🇳 Part III: World & India GK": ["World: Continents, Oceans & Winds", "World: Environment & Migration", "India: Physical features & Climate", "Indian Economy & Foreign Trade"],
    "📜 Part III: Constitution": ["Constituent Assembly & B.R. Ambedkar", "Fundamental Rights & DPSP", "President, PM & Parliament", "Foreign Policy & Neighbors"],
    "🧠 Part IV: Psychology": ["Nature, Scope & Holistic Development", "Learning Theories", "Personality & Mental Health", "Intelligence & Creativity", "Motivation & Individual Differences"]
}

# --- 4. SIDEBAR WITH MODEL SELECTOR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/book.png", width=80)
    st.title("Study Dashboard")
    
    st.markdown("### ⚙️ AI Model Setup")
    # Best models ki dictionary list se filter ki gayi hai
    available_models = {
        "Gemini 3.1 Pro Preview (Best for Quality)": "gemini-3.1-pro-preview",
        "Gemini 3 Flash Preview (Super Fast)": "gemini-3-flash-preview",
        "Gemini 2.5 Pro (Most Stable)": "gemini-2.5-pro",
        "Gemini 2.5 Flash (Fast & Stable)": "gemini-2.5-flash"
    }
    
    # Dropdown menu for model selection
    selected_model_name = st.selectbox("Choose AI Engine:", list(available_models.keys()))
    selected_model_id = available_models[selected_model_name]
    
    st.success(f"Active: {selected_model_id}")
    st.info("Syllabus version: RPSC 2nd Grade 2025")
    st.markdown("---")
    if st.button("♻️ Naya Test Shuru Karein"):
        st.session_state.test_active = False
        st.rerun()

# --- 5. MAIN DASHBOARD ---
st.title("🎓 RPSC Grade 2 Master (Paper-1)")
st.write("Aapki biwi ki taiyari ke liye official syllabus par aadharit Smart Test Series.")

if not st.session_state.get("test_active"):
    st.subheader("📚 Syllabus se Topic Chunein:")
    cols = st.columns(2)
    for i, (main_topic, subs) in enumerate(syllabus.items()):
        with cols[i % 2]:
            with st.expander(main_topic):
                for sub in subs:
                    if st.button(f"▶ {sub}", key=sub):
                        st.session_state.current_sub = sub
                        st.session_state.test_active = True
                        st.rerun()

# --- 6. PRO TEST GENERATOR ---
if st.session_state.get("test_active"):
    topic = st.session_state.current_sub
    st.header(f"📝 Topic: {topic}")
    
    # Sidebar mein jo model select hua hai, wo yahan use hoga
    model = genai.GenerativeModel(selected_model_id)
    
    prompt = f"""
    Aap ek RPSC (Rajasthan Public Service Commission) ke Paper Setter aur Expert hain. 
    RPSC Senior Teacher (Grade 2) ke Paper-1 ke official syllabus topic '{topic}' par 5 top-level questions banaiye.
    
    IMPORTANT RULES:
    1. Language: Poora test aur explanations shuddh HINDI mein hone chahiye.
    2. Format: RPSC ke latest niyam anusar har sawal ke 5 options (A, B, C, D, E) dein. E option hamesha 'Anuttarit Prashna' (अनुत्तरित प्रश्न) hona chahiye.
    3. PYQ Reference: Agar ye question pichle RPSC Grade 2 exams mein aaya hai toh mention karein.
    4. Explanations: Har sawal ke jawab ke baad ek 'Vishleshan' (Detail Explanation) dein jisme us topic ka poora concept clear ho jaye.
    5. Scoring Warning: +2 marks for correct, -1/3 for wrong.
    """
    
    with st.spinner(f"{selected_model_id} RPSC pattern par '{topic}' ke sawal taiyar kar raha hai..."):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error aagaya: {e}. Model change karke try karein.")
    
    if st.button("⬅️ Wapas Syllabus List Par Jayein"):
        st.session_state.test_active = False
        st.rerun()
