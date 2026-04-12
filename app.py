import streamlit as st
import json
import os
from datetime import datetime

# 1. Настройки на страницата
st.set_page_config(page_title="AI Ultra Intelligence", page_icon="🧠", layout="centered")

# 2. Стилизиране (CSS) - Напълно изчистен дизайн
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
        font-size: 18px;
        font-weight: bold;
        margin-top: 15px;
        border-bottom: 1px solid #30363d;
        padding-bottom: 5px;
    }
    .market-badge {
        background-color: #1f2937;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #10b981;
        color: #10b981;
        font-size: 14px;
    }
    /* Стил за текста на анализа, който премахва черните кутии */
    .analysis-body {
        color: #c9d1d9;
        font-size: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 AI Football Deep-Intelligence")
st.write(f"📊 **Системен анализ за:** {datetime.now().strftime('%d.%m.%Y')}")
st.divider()

# 3. Функция за зареждане на данни
def load_data():
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

# 4. Функция за почистване и превод на български
def clean_and_translate(text):
    if not text: return ""
    # Автоматичен превод на термини
    translations = {
        "(Out)": "(Аут - контузен)",
        "(Doubtful)": "(Под въпрос)",
        "(Suspended)": "(Наказан)",
        "(Returning)": "(Завръща се)",
        "minor knock": "лека травма",
        "from suspension": "след наказание",
        "---": "",
        "###": "",
        "</div>": "",
        "<div>": ""
    }
    for eng, bg in translations.items():
        text = text.replace(eng, bg)
    return text.strip()

# 5. Визуализация
matches = load_data()

if not matches:
    st.info("🕒 AI Анализаторът подготвя докладите...")
else:
    for m in matches:
        # Основна карта на мача
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
            # 1. ТАКТИЧЕСКА ОБОСНОВКА
            st.markdown("<div class='section-header'>🔍 1. Пълна Обосновка</div>", unsafe_allow_html=True)
            # Използваме st.text за избягване на автоматичното форматиране като код
            cleaned_strat = clean_and_translate(m.get('strat', ''))
            st.write(cleaned_strat)
            
            # 2. КАДРОВА СИТУАЦИЯ
            st.markdown("<div class='section-header'>🚑 2. Състави и Липсващи Играчи</div>", unsafe_allow_html=True)
            st.warning(clean_and_translate(m.get('injuries', 'Няма липсващи.')))
            
            # 3. СЪДИЯ И ПСИХОЛОГИЯ
            st.markdown("<div class='section-header'>⚖️ 3. Съдия и Напрежение</div>", unsafe_allow_html=True)
            st.write(clean_and_translate(m.get('ref', 'Информацията се обновява...')))
            
            # 4. АЛТЕРНАТИВНИ ПАЗАРИ
            if 'other' in m:
                st.markdown("<div class='section-header'>📊 4. Алтернативни Вероятности</div>", unsafe_allow_html=True)
                for market, prob in m['other'].items():
                    st.write(f"🔹 {market}: **{prob}**")

st.divider()
st.caption("Верифициран AI анализ | Всички права запазени")
