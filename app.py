import streamlit as st
import json
import os

# Оптимизация на страницата за мобилни устройства
st.set_page_config(page_title="AI Ultra Stats", layout="centered")

# CSS за изчистен и модерен вид
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .main-title { font-size: 22px !important; color: #00ff41; text-align: center; font-weight: bold; margin-bottom: 20px; }
    /* Настройка на падащите менюта */
    .stExpander { border: 1px solid #30363d !important; background-color: #161b22 !important; border-radius: 8px !important; margin-bottom: 5px !important; }
    .stMarkdown p { font-size: 14px; line-height: 1.5; }
    .label { font-weight: bold; color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ AI Експертни Анализи & Прогнози</div>', unsafe_allow_html=True)

def load_data():
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

data = load_data()

if not data:
    st.info("🔄 Системата сканира интернет за мачове... Моля, изчакайте GitHub Action да приключи.")
else:
    for m in data:
        # Падащо меню с малко заглавие (Мач | Коефициент)
        header = f"📌 {m['match']} | {m.get('market', 'Анализ')}"
        with st.expander(header):
            # Секция: Информация
            st.markdown(f"<span class='label'>🏆 Лига/Час:</span> {m['prob']}", unsafe_allow_html=True)
            
            st.divider()
            
            # Секция: Дълбок анализ (основен текст)
            st.markdown("<span class='label'>🧠 Дълбок Анализ и Обосновка:</span>", unsafe_allow_html=True)
            st.write(m['strat'])
            
            st.divider()
            
            # Секция: Състави и Рефер
            col1, col2 = st.columns(2)
            with col1:
                st.warning(f"📋 **Състави:**\n{m['injuries']}")
            with col2:
                st.info(f"⚖️ **Рефер:**\n{m['ref']}")
            
            # Секция: Финална Прогноза
            st.success(f"🎯 **Експертна Прогноза:** {m['tip']}")
            
            if "other" in m:
                st.caption(f"🕒 Последна актуализация на данните: {m['other'].get('Time', 'Днес')}")

st.sidebar.markdown("---")
st.sidebar.caption("Данните се генерират чрез Google Search Retrieval в реално време.")
