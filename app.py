import streamlit as st
import json
import os

st.set_page_config(page_title="AI Ultra Predictor", page_icon="⚽", layout="centered")

# Модерен тъмен стил
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stExpander { border: 1px solid #30363d !important; background-color: #161b22 !important; border-radius: 10px !important; }
    .main-title { color: #00ff41; font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">⚽ AI АВТОНОМНИ ПРОГНОЗИ</p>', unsafe_allow_html=True)

if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for m in data:
        with st.expander(f"📋 {m['match']} | {m['prob']}"):
            st.subheader("📝 Експертна Обосновка")
            st.write(m['strat'])
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🚑 **Състави & Контузии:**\n{m['injuries']}")
            with col2:
                st.warning(f"⚖️ **Съдия & Дисциплина:**\n{m['ref']}")
            
            st.divider()
            
            st.success(f"🎯 **ФИНАЛНА ПРОГНОЗА:** {m['tip']}")
            st.markdown(f"📊 **Коефициент:** {m['market']}")
else:
    st.warning("🔄 В момента AI агентът анализира мачовете за деня. Моля, освежете след минута.")
