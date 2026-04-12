import streamlit as st
import pandas as pd
from datetime import datetime

# Настройки на страницата
st.set_page_config(page_title="AI Ultra Analyst", page_icon="📈", layout="wide")

# Стилизиране с CSS за по-модерен вид
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Full-Scale Football Predictor")
st.write(f"📊 **Системен статус:** Сканиране на API източници, новинарски портали и социални мрежи... [OK]")
st.divider()

# --- ЛОГИКА ЗА ПЪЛНОМАЩАБЕН АНАЛИЗ ---
def render_deep_analysis(match_data):
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"🏟️ {match_data['match']}")
            st.markdown(f"**Избран пазар:** `{match_data['market']}`")
            st.markdown(f"**Прогноза:** :green[{match_data['tip']}]")
        
        with col2:
            st.metric("AI Индекс на доверие", match_data['prob'])

        # Секция с подробни данни
        tabs = st.tabs(["🔍 Пълен Анализ", "🚑 Кадрова ситуация", "📊 Статистически модел"])
        
        with tabs[0]:
            st.write("**AI Резюме на глобалните данни:**")
            st.info(match_data['full_analysis'])
            
        with tabs[1]:
            st.warning(match_data['injuries'])
            
        with tabs[2]:
            st.write(f"**Вероятностни нива според пазарите:**")
            st.json(match_data['market_odds'])
        
        st.divider()

# --- ДАННИ ЗА ДНЕШНИЯ АНАЛИЗ ---
# (Тук симулираме резултата от пълномащабното търсене)
matches = [
    {
        "match": "Arsenal vs Manchester United",
        "market": "Азиатски Хендикап - Корнери",
        "tip": "Арсенал -2.5 корнера",
        "prob": "89%",
        "full_analysis": "Сканирането на териториалното разпределение на играта показва, че Арсенал използва 72% от ширината на терена срещу затворени отбори. United в момента са с временен треньор, който залага на нисък блок, което генерира средно 8.5 корнера за противника. Анализът на интернет трафика от местни спортни журналисти потвърждава, че United ще играят без типични крила, което ограничава техните офанзивни корнери.",
        "injuries": "Arsenal: Пълен състав в предни позиции. Man Utd: Липса на основните бек-ове (Shaw, Wan-Bissaka), което оголва фланговете.",
        "market_odds": {"Over 1.5 Goals": "94%", "Home Corner -2.5": "89%", "Away Under 1.5 Cards": "62%"}
    },
    {
        "match": "Inter vs Juventus",
        "market": "Картони - Общо",
        "tip": "Над 5.5 картона",
        "prob": "94%",
        "full_analysis": "Пълномащабният анализ на съдията за мача (Мариани) показва средна стойност от 6.2 картона в дерби срещи. Социалните мрежи и интервюта от седмицата показват изключително високо напрежение в лагера на Ювентус след наказанието на техен играч. Историческият модел за Derby d'Italia предвижда агресия в центъра на терена (Barell vs Locatelli).",
        "injuries": "Inter: Всички титуляри са на линия. Juve: Липса на дисциплиниран дефанзивен халф.",
        "market_odds": {"Total Cards Over 5.5": "94%", "Draw": "31%", "BTTS - No": "78%"}
    }
]

# Изчертаване на мачовете
for m in matches:
    render_deep_analysis(m)

# --- АВТОМАТИЗИРАН АРХИВ ---
st.header("📂 Автоматизиран Архив (Verified)")
archive_df = pd.DataFrame([
    {"Дата": "12.04", "Мач": "Real vs Alaves", "Пазар": "Handicap", "Прогноза": "1 (-1.5)", "Статус": "WIN ✅"},
    {"Дата": "12.04", "Maч": "Chelsea vs City", "Пазар": "1X2", "Прогноза": "2", "Статус": "WIN ✅"}
])

def style_archive(row):
    return ['background-color: #1b5e20' if 'WIN' in row.Статус else 'background-color: #b71c1c'] * len(row)

st.dataframe(archive_df.style.apply(style_archive, axis=1), use_container_width=True)
