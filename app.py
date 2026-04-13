import streamlit as st
import json
import os

# Настройка на страницата
st.set_page_config(
    page_title="AI Football Expert",
    page_icon="⚽",
    layout="centered" # "centered" прави всичко по-прибрано и по-малко
)

# Стилизиране с CSS за по-малки шрифтове и по-красиви карти
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ AI Професионални Прогнози")
st.subheader("Потвърдени състави, съдии и задълбочен анализ")

# Функция за зареждане на данни
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

data = load_data()

if not data:
    st.warning("⚠️ В момента данните се обновяват от изкуствения интелект. Моля, опитайте след минута.")
else:
    # Показване на мачовете в компактен вид
    for item in data:
        # Използваме expander, за да намалим размера на полетата
        with st.expander(f"📌 {item['match']} | {item.get('market', '')}"):
            
            # Разделяме на две колони за по-добър изглед
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**🏆 Лига:** {item['prob']}")
                st.markdown(f"**🧠 Експертен Анализ:**")
                st.write(item['strat'])
            
            with col2:
                st.success(f"**🎯 Прогноза:**\n\n{item['tip']}")
                st.info(f"**⚖️ Рефер:**\n\n{item['ref']}")

            st.divider()
            
            # Секция за състави (жълто поле)
            st.warning(f"📋 **Потвърдена информация и състави:**\n\n{item['injuries']}")
            
            # Допълнителна статистика (ако има)
            if "other" in item:
                st.caption(f"🕒 Последна актуализация: {item['other'].get('Time', '---')}")

st.sidebar.markdown("---")
st.sidebar.write("🤖 **Система:** Gemini 1.5 Pro")
st.sidebar.write("🌐 **Източник:** Търсене в реално време")
st.sidebar.info("Данните се обновяват на всеки час с най-новите новини от спортните медии.")
