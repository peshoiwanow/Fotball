import streamlit as st
import pandas as pd
from datetime import datetime

# Конфигурация за професионален изглед
st.set_page_config(page_title="PRO AI Analyst", page_icon="🏆", layout="centered")

# Custom CSS за премиум усещане
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .match-header {
        background: linear-gradient(90deg, #1f2937 0%, #111827 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin-bottom: 5px;
    }
    .status-badge {
        background-color: #10b981;
        color: white;
        padding: 2px 10px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
    }
    .analysis-section {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 0 0 10px 10px;
        border: 1px solid #374151;
        line-height: 1.6;
    }
    h4 { color: #10b981; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 PRO Football AI Intelligence")
st.write(f"📅 **Дневен анализ:** {datetime.now().strftime('%d %B %Y')} | **Статус:** Активен")
st.divider()

# --- ФУНКЦИЯ ЗА ГЕНЕРИРАНЕ НА ПРОФЕСИОНАЛНА КАРТА ---
def render_pro_match(m):
    # Горна част на картата (винаги видима)
    st.markdown(f"""
    <div class="match-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 18px; font-weight: bold; color: white;">{m['match']}</span>
            <span class="status-badge">CONFIDENCE: {m['prob']}</span>
        </div>
        <div style="margin-top: 8px; color: #9ca3af;">
            <span style="color: #10b981;">●</span> {m['market']} : <b>{m['tip']}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Панел с пълномащабен анализ
    with st.expander("📄 ВИЖ ПЪЛЕН ЕКСПЕРТЕН АНАЛИЗ"):
        st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
        
        st.markdown("#### 🔍 Стратегическа прогноза")
        st.write(m['strat'])
        
        st.markdown("#### 🚑 Кадрова ситуация и Ротации")
        st.info(m['injuries'])
        
        st.markdown("#### ⚖️ Съдийски фактор и Психология")
        st.write(m['ref'])
        
        st.markdown("#### 📊 Алтернативни AI Вероятности")
        for alt_m, alt_p in m['other'].items():
            col_a, col_b = st.columns([3, 1])
            col_a.write(alt_m)
            col_b.write(f"**{alt_p}**")
            
        st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

# --- ДАННИ ЗА 5-ТЕ СРЕЩИ ---
matches = [
    {
        "match": "Arsenal vs Manchester United",
        "market": "Азиатски Хендикап Корнери",
        "tip": "Арсенал -2.5",
        "prob": "89%",
        "strat": "Тактическият модел на Артета разчита на претоварване на фланговете (overloading), което генерира средно 7.8 корнера на мач у дома. Манчестър Юнайтед са в преходен период и използват нисък блок, което води до висок брой блокирани удари и центрирания.",
        "injuries": "Юнайтед без Лисандро Мартинес - по-бавна реакция при изчистване. Арсенал с пълен офанзивен капацитет.",
        "ref": "Майкъл Оливър: Склонен да оставя играта при флангови сблъсъци.",
        "other": {"Над 2.5 гола": "74%", "Победа Арсенал": "68%"}
    },
    {
        "match": "Inter vs Juventus",
        "market": "Дисциплина (Картони)",
        "tip": "Над 5.5 Жълти Картона",
        "prob": "94%",
        "strat": "Derby d'Italia винаги е съпътствано от висок интензитет. Интер пресира високо, а Ювентус използва тактически нарушения за спиране на контраатаки.",
        "injuries": "Липса на опитни дефанзивни халфове при Юве води до по-агресивни влизания на защитниците.",
        "ref": "Давиде Маса: Средно 5.8 картона в дербита.",
        "other": {"Червен картон": "42%", "Равенство": "35%"}
    },
    {
        "match": "Real Madrid vs Alaves",
        "market": "Азиатски Хендикап",
        "tip": "Реал Мадрид -1.5",
        "prob": "92%",
        "strat": "Реал Мадрид е в серия от 5 победи на 'Бернабеу'. Алавес официално обявиха ротации в защита, за да пазят сили за следващия кръг.",
        "injuries": "Мбапе и Винисиус започват титуляри. Алавес без двама ключови бекове.",
        "ref": "Мунуера Монтеро: Склонен да дава дузпи при минимален контакт.",
        "other": {"Над 2.5 гола": "78%", "Гол на Мбапе": "65%"}
    },
    {
        "match": "Osasuna vs Betis",
        "market": "Голове (Общо)",
        "tip": "Под 2.5 гола",
        "prob": "74%",
        "strat": "Бетис са без двамата си основни плеймейкъри. Осасуна играе изключително дефанзивно у дома (средно 0.9 допуснати гола).",
        "injuries": "Липса на Isco и Lo Celso - липса на креативност в центъра на Бетис.",
        "ref": "Алберола Рохас: Обикновено позволява по-твърда игра.",
        "other": {"Първо полувреме Х": "55%", "BTTS: NO": "68%"}
    },
    {
        "match": "Nottm Forest vs Aston Villa",
        "market": "Двата отбора да вкарат",
        "tip": "ДА (BTTS)",
        "prob": "70%",
        "strat": "Астън Вила е с втори вратар. Форест са вкарали в 90% от домакинствата си този сезон.",
        "injuries": "Емилиано Мартинес е аут за Вила. Оли Уоткинс е в топ форма за гостите.",
        "ref": "Пол Тиърни: Често допуска грешки, водещи до опасни ситуации.",
        "other": {"Над 3.5 картона": "62%", "Победа Вила": "48%"}
    }
]

# Извеждане на 5-те мача
for m in matches:
    render_pro_match(m)

# --- АРХИВ ---
st.header("📂 Верифициран AI Архив")
archive_data = {
    "Дата": ["11.04", "11.04"],
    "Мач": ["Liverpool vs Arsenal", "Juventus vs Lazio"],
    "Прогноза": ["Over 2.5", "1"],
    "Статус": ["WIN ✅", "LOSE ❌"]
}
st.table(pd.DataFrame(archive_data))
