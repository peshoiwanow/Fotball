import streamlit as st
import json
import os
from datetime import datetime
import re

# 1. Настройки на страницата
st.set_page_config(page_title="AI Ultra Intelligence", page_icon="🧠", layout="centered")

# 2. Стилизиране (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; }
    .report-card {
        background: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        border-left: 5px solid #00ff88;
        margin-bottom: 15px;
    }
    .confidence-score { color: #00ff88; font-weight: 900; font-size: 24px; }
    .section-header {
        color: #58a6ff;
        font-size: 19px;
        font-weight: bold;
        margin-top: 20px;
        border-bottom: 2px solid #30363d;
        padding-bottom: 8px;
        margin-bottom: 10px;
    }
    .market-badge {
        background-color: #1f2937;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #10b981;
        color: #10b981;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 AI Football Deep-Intelligence")
st.write(f"📊 **Системен анализ за:** {datetime.now().strftime('%d.%m.%Y')}")
st.divider()

# 3. Зареждане на данни
def load_data():
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

# 4. Функция за "Разкрасяване" на текста (Маха прозорците и превежда)
def format_clean_text(text):
    if not text: return ""
    
    # 1. Премахваме излишните интервали в началото на всеки нов ред (това маха черните кутии)
    lines = [line.strip() for line in text.split('\n')]
    text = "\n".join(lines)
    
    # 2. Автоматичен превод на термини
    replacements = {
        "(Out)": "🔴 (Аут)",
        "(Doubtful)": "🟡 (Под въпрос)",
        "(Suspended)": "🚫 (Наказан)",
        "(Returning)": "🟢 (Завръща се)",
        "---": "", "###": "", "</div>": "", "<div>": ""
    }
    for eng, bg in replacements.items():
        text = text.replace(eng, bg)
    
    return text

# 5. Визуализация
matches = load_data()

if not matches:
    st.info("🕒 AI Анализаторът подготвя докладите...")
else:
    for m in matches:
        # Основна карта
        st.markdown(f"""
        <div class="report-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 20px; font-weight: bold; color: white;">🏟️ {m.get('match')}</span>
                <span class="confidence-score">{m.get('prob')}</span>
            </div>
            <div style="margin-top: 10px; display: flex; gap: 10px; align-items: center;">
                <span class="market-badge">{m.get('market')}</span>
                <b style="color:white">Прогноза: {m.get('tip')}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📄 ВИЖ ПЪЛЕН ЕКСПЕРТЕН АНАЛИЗ"):
            # Изчистване на текстовете
            full_analysis = format_clean_text(m.get('strat', ''))
            injuries = format_clean_text(m.get('injuries', 'Няма данни.'))
            referee = format_clean_text(m.get('ref', 'Информацията се обновява.'))

            # Секция 1: Тактика и Обосновка
            st.markdown("<div class='section-header'>🔍 1. Пълна Обосновка</div>", unsafe_allow_html=True)
            st.write(full_analysis) # st.write изобразява чист текст без кутии
            
            # Секция 2: Състави
            st.markdown("<div class='section-header'>🚑 2. Състави и Липсващи Играчи</div>", unsafe_allow_html=True)
            st.warning(injuries)
            
            # Секция 3: Рефер
            st.markdown("<div class='section-header'>⚖️ 3. Съдия и Напрежение</div>", unsafe_allow_html=True)
            st.write(referee)
            
            # Секция 4: Други
            if 'other' in m:
                st.markdown("<div class='section-header'>📊 4. Алтернативни Вероятности</div>", unsafe_allow_html=True)
                for market, prob in m['other'].items():
                    st.write(f"🔹 {market}: **{prob}**")

st.divider()
st.caption("Верифициран AI анализ | Ежедневно обновяване")
