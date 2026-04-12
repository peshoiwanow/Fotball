import streamlit as st
import pandas as pd

# Настройка на темата и заглавието
st.set_page_config(page_title="Football AI Predictor", page_icon="⚽", layout="centered")

# Дизайн на заглавието
st.title("⚽ Football AI Predictor")
st.write(f"Анализирани срещи за: **{pd.Timestamp.now().strftime('%d.%m.%regular%Y')}**")
st.markdown("---")

# --- СЕКЦИЯ 1: ТОП 5 ПРОГНОЗИ ---
st.header("💎 Топ 5 Най-сигурни Прогнози")

# База данни с прогнозите (тук се свързва с твоя скрапер по-късно)
top_5_data = [
    {
        "match": "Chelsea vs Manchester City",
        "tip": "Победа за Manchester City",
        "prob": 88,
        "analysis": "Енцо Фернандес е отстранен от Челси, а Рийс Джеймс е контузен. Сити са в пълен състав и имат 4 поредни победи като гост на Стамфорд Бридж."
    },
    {
        "match": "Osasuna vs Betis",
        "tip": "Под 2.5 гола",
        "prob": 74,
        "analysis": "Бетис играят без Иско и Ло Селсо. Осасуна е един от най-ниско резултатните домакини този сезон. Очаква се затворена игра."
    },
    {
        "match": "Real Madrid vs Alaves",
        "tip": "Победа за Real Madrid (-1.5)",
        "prob": 92,
        "analysis": "Алавес излизат с резервен състав, за да пазят титулярите за мача с Еспаньол. Винисиус и Мбапе са потвърдени титуляри."
    },
    {
        "match": "Sunderland vs Tottenham",
        "tip": "Победа за Tottenham",
        "prob": 81,
        "analysis": "Съндърланд имат криза в защита – двамата титулярни централни защитници са аут. Тотнъм са в пълна бойна готовност."
    },
    {
        "match": "Nottm Forest vs Aston Villa",
        "tip": "Двата отбора да отбележат (Да)",
        "prob": 70,
        "analysis": "Астън Вила са без титулярния си вратар Е. Мартинес. Форест са вкарали гол във всеки един от последните си 8 домакински мача."
    }
]

# Визуализация на прогнозите
for item in top_5_data:
    with st.container():
        # Ред със заглавие и процент
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(item["match"])
        with col2:
            st.metric("Шанс", f"{item['prob']}%")
        
        st.write(f"🎯 **Прогноза:** {item['tip']}")
        
        # Скрит анализ (Expander)
        with st.expander("🧐 Виж пълен анализ на съставите"):
            st.info(item["analysis"])
        
        st.markdown("---")

# --- СЕКЦИЯ 2: АРХИВ ---
st.header("📂 Архив на прогнозите")

# Данни за архива
archive_results = [
    {"Дата": "11.04", "Мач": "Liverpool vs Arsenal", "Прогноза": "Над 2.5", "Резултат": "2:2", "Статус": "WIN ✅"},
    {"Дата": "11.04", "Мач": "Juventus vs Lazio", "Прогноза": "1", "Резултат": "0:1", "Статус": "LOSE ❌"},
    {"Дата": "10.04", "Мач": "Monaco vs Lille", "Прогноза": "Д/Д (Да)", "Резултат": "1:1", "Статус": "WIN ✅"},
    {"Дата": "10.04", "Мач": "Porto vs Benfica", "Прогноза": "Под 3.5", "Резултат": "1:0", "Статус": "WIN ✅"},
]

df = pd.DataFrame(archive_results)

# Функция за оцветяване на редовете
def apply_color(row):
    if "WIN" in row["Статус"]:
        return ['background-color: #d4edda'] * len(row)
    else:
        return ['background-color: #f8d7da'] * len(row)

# Показване на архива
st.dataframe(df.style.apply(apply_color, axis=1), use_container_width=True)

st.caption("Данните се обновяват автоматично след края на всеки мач.")
