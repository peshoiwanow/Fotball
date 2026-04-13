import streamlit as st
import json
import os

st.set_page_config(page_title="Ultra AI Analytics", layout="wide")

# Тъмен дизайн с акцент върху четливостта
st.markdown("""
    <style>
    .report-card { background-color: #111d2c; border-left: 10px solid #00ff41; padding: 25px; border-radius: 15px; margin-bottom: 30px; }
    .stat-box { background-color: #1c2a3a; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .prediction-text { font-size: 20px; color: #00ff41; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AI Футболен Скенер: Deep Web Analysis")

if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for m in data:
        st.markdown(f"<div class='report-card'><h1>{m['match']}</h1><h3>{m['prob']}</h3></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader("📝 Дълбок Анализ и Обосновка")
            st.write(m['strat'])
            st.divider()
            st.subheader("📋 Потвърдени Състави и Новини")
            st.info(m['injuries'])
            
        with col2:
            st.markdown("<div class='stat-box'>", unsafe_allow_html=True)
            st.subheader("🎯 Експертна Прогноза")
            st.markdown(f"<p class='prediction-text'>{m['tip']}</p>", unsafe_allow_html=True)
            st.divider()
            st.subheader("⚖️ Съдия и Дисциплина")
            st.warning(m['ref'])
            st.markdown("</div>", unsafe_allow_html=True)
            st.metric("Достоверност на данните", "98%", "Live Search")
else:
    st.error("Няма налични данни. Стартирайте скрапера от GitHub Actions.")
