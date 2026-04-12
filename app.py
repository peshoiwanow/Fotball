import streamlit as st
import json
import os
from datetime import datetime, date

# 1. Основна конфигурация на страницата
st.set_page_config(page_title="AI Ultra Intelligence", page_icon="🧠", layout="centered")

# 2. Стилизиране с професионален тъмен дизайн (CSS)
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
    /* Стил за бутоните за навигация */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #21262d;
        color: white;
        border: 1px solid #30363d;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00ff88;
        color: #00ff88;
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Функция за зареждане на данни от файловете
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []
    return []

# 4. Функция за интелигентно почистване и превод на български
def super_clean(text):
    if not text: return ""
    
    # Списък за автоматичен превод и почистване на специфични фрази
    replacements = {
        "(Out)": "🔴 (Аут)",
        "(Doubtful)": "🟡 (Под въпрос)",
        "(Suspended)": "🚫 (Наказан)",
        "(Returning from suspension but with minor knock)": "🟢 (Завръща се, но с лека травма)",
        "minor knock": "лека травма",
        "---": "", "###": "", "</div>": "", "<div>": ""
    }
    
    for eng, bg in replacements.items():
        text = text.replace(eng, bg)
    
    # Махаме излишните интервали в началото, за да няма "черни кутии"
    lines = [line.strip() for line in text.split('\n')]
    return "\n".join(lines).strip()

# --- ГОРНА ЧАСТ: БУТОНИ ЗА НАВИГАЦИЯ ---
st.title("🧠 AI Football Deep-Intelligence")

col1, col2 = st.columns(2)

# Инициализация на състоянието на изгледа
if 'view' not in st.session_state:
    st.session_state.view = 'today'

with col1:
    if st.button("🏟️ АНАЛИЗИ ЗА ДНЕС"):
        st.session_state.view = 'today'

with col2:
    if st.button("📂 АРХИВ (КАЛЕНДАР)"):
        st.session_state.view = 'archive'

st.divider()

# --- ЛОГИКА ЗА ИЗБОРА НА ДАННИ ---

if st.session_state.view == 'today':
    st.subheader(f"📊 Текущи анализи: {date.today().strftime('%d.%m.%Y')}")
    matches = load_data('data.json')
    if not matches:
        st.info("🕒 В момента AI генерира новите доклади. Моля, проверете след малко.")
else:
    st.subheader("📂 Календарен архив")
    selected_date = st.date_input("Избери дата за преглед на историята:", date.today())
    # Търсим файла в папката archive
    file_name = f"archive/matches_{selected_date.strftime('%Y-%m-%d')}.json"
    matches = load_data(file_name)
    if not matches:
        st.warning(f"Няма открити данни в архива за {selected_date.strftime('%d.%m.%Y')}")

# --- ВИЗУАЛИЗАЦИЯ НА ДОКЛАДИТЕ ---
for m in matches:
    # Главна карта на мача
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

    # Детайлен експертен анализ (Expander)
    with st.expander("📄 ВИЖ ПЪЛЕН ЕКСПЕРТЕН АНАЛИЗ"):
        # 1. ТАКТИКА
        st.markdown("<div class='section-header'>🔍 1. Пълна Обосновка</div>", unsafe_allow_html=True)
        st.write(super_clean(m.get('strat', '')))
        
        # 2. СЪСТАВИ
        st.markdown("<div class='section-header'>🚑 2. Състави и Липсващи Играчи</div>", unsafe_allow_html=True)
        st.warning(super_clean(m.get('injuries', 'Няма нови липсващи играчи.')))
        
        # 3. РЕФЕР
        st.markdown("<div class='section-header'>⚖️ 3. Съдия и Напрежение</div>", unsafe_allow_html=True)
        st.write(super_clean(m.get('ref', 'Информацията ще се обнови преди началото.')))
        
        # 4. АЛТЕРНАТИВНИ ПАЗАРИ
        if 'other' in m:
            st.markdown("<div class='section-header'>📊 4. Алтернативни Вероятности</div>", unsafe_allow_html=True)
            for market, prob in m['other'].items():
                st.write(f"🔹 {market}: **{prob}**")

st.divider()
st.caption("Системата използва Deep Learning за анализ на тактически модели в реално време.")
