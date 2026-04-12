import streamlit as st
import pandas as pd

# Конфигурация
st.set_page_config(page_title="AI Analyst Pro", page_icon="⚽")

st.title("⚽ Football AI Analyst Pro")
st.info("Днешните топ 5 прогнози са подбрани на база липсващи играчи и форма.")

# --- ПРОГНОЗИ ---
st.header("💎 Топ 5 Прогнози")

# Тези данни по-късно ще ги пълним автоматично
picks = [
    {"match": "Chelsea vs Man City", "tip": "2", "prob": "88%", "analysis": "Челси без Енцо и Рийс Джеймс. Сити са в пълен състав."},
    {"match": "Real Madrid vs Alaves", "tip": "1 (-1.5)", "prob": "92%", "analysis": "Алавес излизат с резерви. Мбапе и Винисиус са титуляри."},
    {"match": "Sunderland vs Tottenham", "tip": "2", "prob": "81%", "analysis": "Криза в защитата на домакините (2-ма контузени)."},
    {"match": "Osasuna vs Betis", "tip": "Under 2.5", "prob": "74%", "analysis": "Бетис без Иско и Ло Селсо - липса на идеи в атака."},
    {"match": "Nottm Forest vs Villa", "tip": "Г/Г (Да)", "prob": "70%", "analysis": "Вила без титулярния си вратар Е. Мартинес."}
]

for p in picks:
    with st.container():
        c1, c2 = st.columns([3, 1])
        c1.subheader(p["match"])
        c2.metric("Вероятност", p["prob"])
        st.write(f"🎯 **Прогноза:** {p['tip']}")
        with st.expander("🧐 Детайлен анализ"):
            st.write(p["analysis"])
        st.divider()

# --- АРХИВ ---
st.header("📂 Архив")
history = {
    "Дата": ["11.04", "11.04", "10.04"],
    "Мач": ["Liverpool vs Arsenal", "Juventus vs Lazio", "Monaco vs Lille"],
    "Прогноза": ["Над 2.5", "1", "Г/Г"],
    "Резултат": ["2:2", "0:1", "1:1"],
    "Статус": ["WIN ✅", "LOSE ❌", "WIN ✅"]
}
df = pd.DataFrame(history)

# Оцветяване
def style_status(val):
    color = 'background-color: #d4edda' if 'WIN' in val else 'background-color: #f8d7da'
    return color

st.dataframe(df.style.applymap(style_status, subset=['Статус']), use_container_width=True)
