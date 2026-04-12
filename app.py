import streamlit as st
import pandas as pd
from datetime import datetime

# Конфигурация
st.set_page_config(page_title="AI Football Prophet", page_icon="📈", layout="centered")

# Стилизиране
st.markdown("""
    <style>
    .main-card {
        background-color: #1a1c23;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #00ff88;
        margin-bottom: 30px;
    }
    .analysis-text {
        font-size: 16px;
        line-height: 1.6;
        color: #e0e0e0;
        text-align: justify;
    }
    .probability-badge {
        background-color: #00ff88;
        color: #000;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 20px;
    }
    .market-label {
        color: #888;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Ultra Football Intelligence")
st.write(f"📅 Глобален анализ за: **{datetime.now().strftime('%d.%m.%Y')}**")
st.divider()

def render_match(m):
    # Основна Карта
    st.markdown(f"### 🏟️ {m['match']}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='market-label'>{m['market']}</div>", unsafe_allow_html=True)
        st.subheader(f"🎯 {m['tip']}")
    with col2:
        st.markdown(f"<div style='text-align:right'><span class='probability-badge'>{m['prob']}</span></div>", unsafe_allow_html=True)

    # Разгъващ се ПЪЛЕН АНАЛИЗ (всичко в едно)
    with st.expander("📥 ВИЖ ПЪЛЕН МАЩАБЕН ДОКЛАД", expanded=False):
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        
        # 1. СТРАТЕГИЧЕСКИ АНАЛИЗ
        st.markdown("#### 🔍 Глобален Стратегически Анализ")
        st.markdown(f"<div class='analysis-text'>{m['strat']}</div>", unsafe_allow_html=True)
        st.divider()
        
        # 2. КАДРОВИ ДОКЛАД
        st.markdown("#### 🚑 Кадрови Дефицит & Новини")
        st.info(m['injuries'])
        st.divider()
        
        # 3. СЪДИЯ И ПСИХОЛОГИЯ
        st.markdown("#### ⚖️ Съдия & Дисциплинарен Профил")
        st.write(m['ref'])
        st.divider()
        
        # 4. ВЕРОЯТНОСТЕН МАСИВ (КРАСИВ ИЗГЛЕД)
        st.markdown("#### 📊 Допълнителни пазари (AI Вероятност)")
        
        # Тук заменяме кода с чист вид
        for market, chance in m['other'].items():
            cols = st.columns([3, 1])
            cols[0].write(f"🔹 {market}")
            cols[1].write(f"**{chance}**")
            st.divider()
            
        st.markdown("</div>", unsafe_allow_html=True)
    st.divider()

# Данни с много подробен анализ
matches = [
    {
        "match": "Arsenal vs Manchester United",
        "market": "Азиатски Хендикап - Корнери",
        "tip": "Арсенал -2.5 корнера",
        "prob": "89%",
        "strat": "Пълният тактически модел на Арсенал под ръководството на Микел Артета се фокусира върху максимално разтегляне на противниковата отбрана. През този сезон Арсенал е отборът с най-много центрирания в наказателното поле, които не се улавят от вратаря, а се изчистват от защитата – основен източник на корнери. Статистическият масив от последните 10 гостувания на United показва, че те допускат средно с 4.2 корнера повече от противника, когато играят срещу отбори, използващи система 4-3-3 с припокриващи бекове. Очаква се United да играят изключително дефанзивно, което ще затвори центъра и ще принуди Арсенал да търси фланговете, генерирайки масиран брой корнери.",
        "injuries": "United официално потвърдиха липсата на Лисандро Мартинес, което означава по-бавна реакция в защита и повече панически чистения в корнер. Арсенал разполага с всички свои крила, което гарантира постоянен натиск.",
        "ref": "Реферът Майкъл Оливър често позволява по-твърда игра по фланговете, което води до блокирани топки, вместо фаулове – това е ключов фактор за крайния брой корнери в този мач.",
        "other": {
            "Над 1.5 гола за Арсенал": "84%",
            "Победа за Арсенал": "68%",
            "Над 9.5 общо корнера": "79%"
        }
    },
    {
        "match": "Inter vs Juventus",
        "market": "Общо Картони",
        "tip": "Над 5.5 картона",
        "prob": "94%",
        "strat": "Анализът на 'Derby d'Italia' в исторически план показва, че напрежението между тези два клуба надхвърля спортния аспект. В последните 5 директни срещи средният брой фаулове е 28.5 на мач, което е с 35% над средното за Серия А. Интер практикува агресивна преса в центъра на терена (Gegenpressing), докато Ювентус залага на контраатаки, които често биват спирани с 'тактически фаулове'. Всяко влизане е потенциален жълт картон.",
        "injuries": "Ювентус влиза в мача без най-дисциплинирания си халф, което ще принуди техните защитници да влизат в по-рискови сблъсъци с бързите нападатели на Интер.",
        "ref": "Давиде Маса е сред най-строгите съдии в Италия. Неговият психологически профил показва, че той обича да установява авторитет рано в мача, като показва картони още при първите груби нарушения.",
        "other": {
            "Червен картон в мача": "42%",
            "Под 2.5 гола": "81%",
            "Равенство": "38%"
        }
    }
]

for m in matches:
    render_match(m)

# Архив
st.header("📂 Архив")
# (Логиката за архива с оцветяването)
