import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- LUXURY CONFIG ---
st.set_page_config(page_title="ELITE EXAM CLOUD", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 40px; font-weight: bold; color: #D4AF37; text-align: center; margin-bottom: 20px; }
    .card { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #D4AF37; margin-bottom: 15px; }
    .stButton>button { background: #D4AF37 !important; color: black !important; border-radius: 20px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SIMULATION ---
# Note: Streamlit Cloud resets every 24h. For permanent 24/7 storage, we use session_state for now.
if 'global_quiz' not in st.session_state: st.session_state.global_quiz = []
if 'global_results' not in st.session_state: st.session_state.global_results = []

st.markdown('<h1 class="main-title">💎 AURORA GLOBAL EXAM</h1>', unsafe_allow_html=True)

# Sidebar for Teacher only
with st.sidebar:
    st.header("⚙️ Control Panel")
    mode = st.radio("Switch View", ["Student Mode", "Teacher Upload", "Admin Dashboard"])
    st.divider()
    st.info("Link copy karke students ko WhatsApp kardein.")

# --- TEACHER UPLOAD (Laptop say karein) ---
if mode == "Teacher Upload":
    st.subheader("📤 Upload Quiz to Cloud")
    t_pass = st.text_input("Teacher Access Key", type="password")
    
    if t_pass == "teacher2024":
        file = st.file_uploader("Upload your MCQ CSV", type="csv")
        if file:
            df = pd.read_csv(file)
            st.session_state.global_quiz = df.to_dict('records')
            st.success("✅ QUIZ LIVE HO GAYA HAI! Ab aap link students ko bhej sakte hain.")
    elif t_pass:
        st.error("Ghalat Password!")

# --- STUDENT MODE (Mobile par chalega) ---
elif mode == "Student Mode":
    if not st.session_state.global_quiz:
        st.warning("⏳ Teacher ne abhi tak quiz upload nahi kiya. Page ko refresh karte rahein.")
    else:
        with st.form("exam_form"):
            st.markdown("### 📝 Entry Form")
            s_name = st.text_input("Apna Full Name likhein")
            st.divider()
            
            answers = {}
            for i, q in enumerate(st.session_state.global_quiz):
                st.markdown(f'<div class="card"><b>Q{i+1}:</b> {q["Question"]}</div>', unsafe_allow_html=True)
                options = [str(q['Option A']), str(q['Option B']), str(q['Option C']), str(q['Option D'])]
                answers[i] = st.radio(f"Select for Q{i+1}", options, key=f"q_{i}", label_visibility="collapsed")
            
            if st.form_submit_button("FINISH TEST"):
                if s_name:
                    score = sum(1 for i, q in enumerate(st.session_state.global_quiz) if answers[i] == str(q['Answer']))
                    st.session_state.global_results.append({
                        "Time": datetime.now().strftime("%H:%M"),
                        "Student": s_name,
                        "Score": f"{score}/{len(st.session_state.global_quiz)}"
                    })
                    st.balloons()
                    st.success(f"Shabash {s_name}! Aapka result save ho gaya hai.")
                else:
                    st.error("Pehle apna naam likhein!")

# --- ADMIN DASHBOARD ---
elif mode == "Admin Dashboard":
    st.subheader("📊 Live Student Progress")
    a_pass = st.text_input("Admin Key", type="password")
    if a_pass == "admin123":
        if st.session_state.global_results:
            st.table(pd.DataFrame(st.session_state.global_results))
        else:
            st.info("Abhi tak kisi student ne test nahi diya.")
