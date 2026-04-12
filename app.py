import streamlit as st
import pandas as pd

# Заглавие
st.title("⚽ Football AI Analyst Pro")
st.markdown("---")

# Секция с прогнози
st.header("💎 Топ 5 Прогнози за Днес")

predictions = [
    {"match": "Chelsea vs Man City", "pred": "Победа за City", "prob": 88, "analysis": "Челси са без Енцо Фернандес. Сити е в пълен състав."},
    {"match": "Real Madrid vs Alaves", "pred": "Реал Мадрид -1.5", "prob": 92, "analysis": "Алавес почиват за следващия кръг."},
    {"match": "Sunderland vs Tottenham", "pred": "Победа за Spurs", "prob": 81, "analysis": "Проблеми в защитата на домакините."},
    {"match": "Osasuna vs Betis", "pred": "Под 2.5 гола", "prob": 74, "analysis": "Липса на креативни халфове в Бетис."},
    {"match": "Nottm Forest vs Villa", "pred": "Д/Д (Да)", "prob": 70, "analysis": "Вила са без титулярния си вратар."}
]

for p in predictions:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(p["match"])
        st.write(f"🎯 Прогноза: **{p['pred']}**")
    with col2:
        st.metric("Шанс", f"{p['prob']}%")
    with st.expander("🧐 Детайлен анализ"):
        st.info(p["analysis"])
    st.markdown("---")

# Секция Архив
st.header("📂 Архив")
data = {
    "Дата": ["11.04", "11.04"],
    "Мач": ["Liverpool vs Arsenal", "Juventus vs Lazio"],
    "Статус": ["WIN ✅", "LOSE ❌"]
}
st.table(pd.DataFrame(data))
