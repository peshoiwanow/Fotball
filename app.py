import streamlit as st
import json
import os

# Настройка на страницата
st.set_page_config(page_title="AI Автономни Прогнози", page_icon="⚽", layout="wide")

st.title("⚽ AI АВТОНОМНИ ПРОГНОЗИ")

def load_data():
    # Проверка дали файлът съществува
    if not os.path.exists('data.json'):
        return None
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

data = load_data()

if not data:
    st.warning("⚠️ В момента няма заредени прогнози. Моля, изчакайте автоматичното обновяване.")
else:
    # Обхождаме всеки мач в JSON файла
    for match in data:
        # Използваме .get(), за да предотвратим KeyError
        m_name = match.get('match', 'Неизвестен мач')
        strat = match.get('strat', 'Няма налична обосновака.')
        injuries = match.get('injuries', 'Няма информация.')
        ref = match.get('ref', 'Няма информация за съдията.')
        tip = match.get('tip', 'В процес на анализ...')
        prob = match.get('prob', 'N/A') # Критичното поле за грешката

        # Дизайн на картата на мача
        with st.expander(f"📋 {m_name}"):
            st.subheader("📝 Експертна Обосновка")
            st.write(strat)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"🚑 **Състави & Контузии:**\n\n{injuries}")
            with col2:
                st.warning(f"⚖️ **Съдия & Дисциплина:**\n\n{ref}")
            
            st.divider()
            
            # Финална секция с прогнозата
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"🎯 **ФИНАЛНА ПРОГНОЗА:** {tip}")
            with c2:
                # Използваме markdown за подчертаване на коефициента
                st.markdown(f"📊 **Коефициент:** `{prob}`")

# Странична лента
st.sidebar.header("За проекта")
st.sidebar.write("Този сайт се обновява автоматично на всеки час чрез AI моделите на Google Gemini.")
st.sidebar.info("Всички прогнози са генерирани от изкуствен интелект на база реални статистически данни.")
