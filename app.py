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
    "⚖️ Polity & Admin": ["Governor & CM", "High Court & Assembly", "Panchayati Raj", "RPSC & Commissions"],
    "🧠 Psychology": ["Learning Theories", "Personality & Mental Health", "Intelligence & Creativity", "Motivation"]
}

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/test.png", width=80)
    st.title("⚙️ Test Settings")
    available_models = {
        "Gemini 3.1 Pro Preview (Best)": "gemini-3.1-pro-preview",
        "Gemini 3 Flash Preview (Fast)": "gemini-3-flash-preview",
        "Gemini 2.5 Pro": "gemini-2.5-pro"
    }
    selected_model_id = available_models[st.selectbox("Select AI Model:", list(available_models.keys()))]
    
    if st.button("♻️ Naya Topic Chunein"):
        st.session_state.test_data = None
        st.session_state.test_active = False
        st.session_state.submitted = False
        st.rerun()

# --- 6. MAIN DASHBOARD ---
if not st.session_state.test_active:
    st.title("🎓 RPSC Grade 2 Premium Test Series")
    st.write("### 📚 Topic select karein aur 5 Minute ka test shuru karein:")
    
    cols = st.columns(2)
    for i, (main_topic, subs) in enumerate(syllabus.items()):
        with cols[i % 2]:
            with st.expander(main_topic):
                for sub in subs:
                    if st.button(f"▶ {sub}", key=sub):
                        st.session_state.current_sub = sub
                        st.session_state.test_active = True
                        st.session_state.submitted = False
                        st.session_state.user_answers = {}
                        st.rerun()

# --- 7. TEST GENERATION & EXECUTION ---
if st.session_state.test_active and not st.session_state.submitted:
    topic = st.session_state.current_sub
    st.header(f"⏱️ Live Test: {topic} (Time: 5 Mins)")
    
    # Generate Questions only if not already generated
    if st.session_state.test_data is None:
        model = genai.GenerativeModel(selected_model_id)
        prompt = f"""
        Aap RPSC 2nd Grade ke expert hain. '{topic}' par exactly 10 questions banaiye.
        
        STRICT RULES & LOGIC:
        1. Question 1: Yeh ek Real Previous Year Question (PYQ) hona chahiye. Question ke ant mein bracket mein (Exam Name aur Year) likhein.
        2. Questions 2, 3, 4, aur 5: Yeh chaar sawal Question 1 ke chaar options (A, B, C, D) par aadharit hone chahiye. Har option ki detail par ek naya sawal banayein.
        3. Questions 6 to 10: Isi topic ke anya mahatvapurn (important) sawal banayein.
        4. Har sawal ke 5 options honge. 5th option hamesha "अनुत्तरित प्रश्न" hoga.
        5. Sab kuch HINDI mein hoga.
        
        OUTPUT FORMAT (Strictly ONLY valid JSON array of objects, no markdown syntax like ```json):
        [
            {{
                "q_no": 1,
                "question": "Sawal likhein... (RPSC 2018)",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4", "अनुत्तरित प्रश्न"],
                "answer_index": 0,
                "explanation": "Detail explanation in Hindi..."
            }}
        ]
        """
        
        with st.spinner("Expert AI Test paper taiyar kar raha hai... Kripya pratiksha karein."):
            try:
                response = model.generate_content(prompt)
                raw_text = response.text.replace('```json', '').replace('```', '').strip()
                st.session_state.test_data = json.loads(raw_text)
                st.session_state.start_time = time.time() # Start Timer
                st.rerun()
            except Exception as e:
                st.error(f"Test banane mein error aaya. Model change karke try karein. Error: {e}")
                if st.button("Wapas Jayein"):
                    st.session_state.test_active = False
                    st.rerun()
                st.stop()

    # Display the Test UI
    if st.session_state.test_data:
        st.warning("⚠️ Dhyan rahe: Test 5 minute ka hai. Sahi jawab par +2, Galat par -0.66 marks.")
        
        with st.form(key="test_form"):
            for q in st.session_state.test_data:
                st.markdown(f"<div class='question-card'><h4>Q{q['q_no']}. {q['question']}</h4></div>", unsafe_allow_html=True)
                # Radio buttons for options
                user_choice = st.radio(
                    "Apna jawab chunein:", 
                    q['options'], 
                    key=f"q_{q['q_no']}",
                    index=None # No default selection
                )
                st.session_state.user_answers[q['q_no']] = user_choice
                st.write("---")
            
            submit_btn = st.form_submit_button("✅ FINAL SUBMIT")
            
            if submit_btn:
                time_taken = time.time() - st.session_state.start_time
                if time_taken > 300: # 5 Minutes = 300 seconds
                    st.error("⏳ Time Up! Aapne 5 minute se zyada waqt liya. Par hum result dikha rahe hain.")
                st.session_state.submitted = True
                st.rerun()

# --- 8. RESULT & EXPLANATION SCREEN ---
if st.session_state.submitted and st.session_state.test_data:
    st.balloons()
    st.header("📊 Aapka Final Result")
    
    score = 0
    correct = 0
    wrong = 0
    unattempted = 0
    
    # Calculate Score
    for q in st.session_state.test_data:
        correct_option_text = q['options'][q['answer_index']]
        user_choice = st.session_state.user_answers.get(q['q_no'])
        
        if user_choice == correct_option_text:
            score += 2
            correct += 1
        elif user_choice == "अनुत्तरित प्रश्न" or user_choice is None:
            unattempted += 1
        else:
            score -= 0.66
            wrong += 1
            
    # Score Board
    st.markdown(f"""
        <div class='score-board'>
            Total Score: {round(score, 2)} / 20 <br>
            <span style='color: green; font-size: 20px;'>✅ Sahi: {correct}</span> | 
            <span style='color: red; font-size: 20px;'>❌ Galat: {wrong}</span> | 
            <span style='color: gray; font-size: 20px;'>⚪ Chhode: {unattempted}</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📝 Vistrit Vishleshan (Detailed Explanations)")
    
    # Show explanations
    for q in st.session_state.test_data:
        correct_option_text = q['options'][q['answer_index']]
        user_choice = st.session_state.user_answers.get(q['q_no'])
        
        st.markdown(f"**Q{q['q_no']}. {q['question']}**")
        
        if user_choice == correct_option_text:
            st.markdown(f"<div class='result-card-correct'>✅ <b>Aapka Jawab:</b> {user_choice} (Bilkul Sahi)<br><br><b>Explanation:</b> {q['explanation']}</div>", unsafe_allow_html=True)
        else:
            ans_display = user_choice if user_choice else "Koi option select nahi kiya"
            st.markdown(f"<div class='result-card-wrong'>❌ <b>Aapka Jawab:</b> {ans_display}<br>✅ <b>Sahi Jawab:</b> {correct_option_text}<br><br><b>Explanation:</b> {q['explanation']}</div>", unsafe_allow_html=True)
        st.write("")
        
    if st.button("🔄 Naya Topic Chunein"):
        st.session_state.test_data = None
        st.session_state.test_active = False
        st.session_state.submitted = False
        st.rerun()
