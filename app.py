import streamlit as st
import json
import os

st.set_page_config(page_title="AI Ultra Predictor", layout="wide")

# Тъмен, модерен дизайн
st.markdown("""
    <style>
    .main { background-color: #0f1116; color: white; }
    .stExpander { border: 1px solid #30363d !important; background-color: #161b22 !important; border-radius: 8px !important; }
    .match-header { font-size: 22px; color: #58a6ff; font-weight: bold; }
    .prediction-box { background-color: #238636; padding: 10px; border-radius: 5px; color: white; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Футболен Анализатор (Live Scanned)")
st.write("Системата сканира Flashscore & SofaScore в реално време за най-добрите залози.")

if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        matches = json.load(f)
    
    for m in matches:
        with st.expander(f"⭐ {m['match']} | {m['prob']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📝 Пълен Анализ")
                st.write(m['strat'])
                st.markdown("---")
                st.markdown("### 📋 Потвърдени Състави")
                st.info(m['injuries'])
            
            with col2:
                st.markdown("### 🎯 Прогноза")
                st.success(m['tip'])
                st.markdown("### ⚖️ Рефер")
                st.warning(m['ref'])
                st.metric("Вероятност (AI)", "Висока")
else:
    st.warning("🔄 AI агентът в момента сканира пазара. Моля, стартирайте GitHub Action.")
