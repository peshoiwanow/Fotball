import streamlit as st
import json
import os
from datetime import datetime

# 1. Основна конфигурация на страницата
st.set_page_config(page_title="AI Ultra Intelligence", page_icon="🧠", layout="centered")

# 2. Стилизиране с професионален дизайн (Тъмна тема и акценти)
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
    .confidence-score {
        color: #00ff88;
        font-weight: 900;
        font-size: 24px;
    }
    .section-header {
        color: #58a6ff;
        font-size: 18px;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
        border-bottom: 1px solid #30363d;
    }
    .analysis-text {
        color: #c9d1d9;
        line-height: 1.6;
        font-size: 15px;
        white-space: pre-line; /* Запазва новите редове без код форматиране */
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

# 3. Функция за зареждане на реалните данни от data.json
def load_data():
    if os.path.exists('data.json'):
        try:
            with open('data.json', 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:
                    return []
                return json.loads(content)
        except Exception:
            return []
    return []

# 4. Функция за визуализация на всеки отделен мач
def render_match(m):
    # Основна карта на мача
    st.markdown(f"""
    <div class="report-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 20px; font-weight: bold; color: white;">🏟️ {m.get('match', 'Няма данни')}</span>
            <span class="confidence-score">{m.get('prob', '-%')}</span>
        </div>
        <div style="margin-top: 10px; display: flex; gap: 10px; align-items: center;">
            <span class="market-badge">{m.get('market', '-')}</span>
            <b style="color:white">Прогноза: {m.get('tip', '-')}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Разгъващ се анализ (Expander)
    with st.expander("📄 ВИЖ ПЪЛЕН ЕКСПЕРТЕН АНАЛИЗ И ОБОСНОВКА"):
        # 1. СТРАТЕГИЧЕСКИ АНАЛИЗ
        st.markdown("<div class='section-header'>🔍 1. Тактическа Обосновка</div>", unsafe_allow_html=True)
        st.write(m.get('strat', 'Анализът се генерира...'))
        
        # 2. КАДРОВА СИТУАЦИЯ
        st.markdown("<div class='section-header'>🚑 2. Състави и Липсващи Играчи</div>", unsafe_allow_html=True)
        injuries = m.get('injuries', 'Няма критични новини.')
        st.warning(injuries)
        
        # 3. РЕФЕР И ПСИХОЛОГИЯ
        st.markdown("<div class='section-header'>⚖️ 3. Съдия и Фактор Напрежение</div>", unsafe_allow_html=True)
        st.write(m.get('ref', 'Информацията ще бъде обновена преди мача.'))
        
        # 4. ДОПЪЛНИТЕЛНИ ВЕРОЯТНОСТИ
        if 'other' in m:
            st.markdown("<div class='section-header'>📊 4. Алтернативни Пазари</div>", unsafe_allow_html=True)
            for market, prob in m['other'].items():
                col1, col2 = st.columns([3, 1])
                col1.write(f"🔹 {market}")
                col2.write(f"**{prob}**")

# 5. Основно изпълнение
matches = load_data()

if not matches:
    st.info("🕒 AI Анализаторът обработва данни в реално време. Прогнозите се обновяват автоматично всяка вечер в 00:00 ч.")
    st.image("https://img.freepik.com/free-vector/artificial-intelligence-robot-working-laptop_107791-16471.jpg")
else:
    for match in matches:
        render_match(match)

# 6. Секция Архив
st.divider()
st.header("📂 История и Резултати")
st.write("Тук автоматично ще се появяват резултатите след приключване на събитията.")
