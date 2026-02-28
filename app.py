import streamlit as st
import google.generativeai as genai
import json
import time

# --- 1. PREMIUM PAGE SETUP & UI ---
st.set_page_config(page_title="RPSC 2nd Grade Pro Test", layout="wide", page_icon="🏆")

st.markdown("""
    <style>
    /* Premium Colors and Cards */
    .stApp { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; font-weight: bold; border: none; font-size: 16px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .question-card { background-color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; border-left: 5px solid #2a5298; }
    .result-card-correct { background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 5px solid #4caf50; margin-top: 10px; }
    .result-card-wrong { background-color: #ffebee; padding: 15px; border-radius: 8px; border-left: 5px solid #f44336; margin-top: 10px; }
    .score-board { font-size: 24px; font-weight: bold; color: #1e3c72; text-align: center; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE API CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ API Key Error: Streamlit Settings > Secrets mein 'GEMINI_API_KEY' set karein.")
    st.stop()

# --- 3. SESSION STATES ---
if "test_data" not in st.session_state: st.session_state.test_data = None
if "test_active" not in st.session_state: st.session_state.test_active = False
if "submitted" not in st.session_state: st.session_state.submitted = False
if "start_time" not in st.session_state: st.session_state.start_time = 0
if "user_answers" not in st.session_state: st.session_state.user_answers = {}

# --- 4. OFFICIAL SYLLABUS DATA ---
syllabus = {
    "🌍 Rajasthan Geography": ["Physical features", "Climate & Drainage", "Agriculture & Livestock", "Tourism & Industries"],
    "🏰 Rajasthan History": ["Ancient Civilizations", "Rajput Dynasties", "1857 Revolution", "Prajamandal Movements", "Integration of Rajasthan"],
    "🎭 Art & Culture": ["Lok Devta & Saints", "Architecture (Forts, Temples)", "Fairs & Festivals", "Customs & Ornaments"],
