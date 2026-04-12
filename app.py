import streamlit as st
import pandas as pd
from datetime import datetime

# Настройки за мобилно устройство и дизайн
st.set_page_config(page_title="AI Football Deep-Dive", page_icon="⚽", layout="centered")

# CSS за премахване на "код" изгледа и професионален дизайн
st.markdown("""
    <style>
    .match-card {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00ff88;
        margin-bottom: 10px;
    }
    .analysis-block {
        background-color: #111b21;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #222;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ AI Full-Scale Analyst")
st.write(f"📅 **Топ 5 Прогнози за деня:** {datetime.now().strftime('%d.%m.%Y')}")
st.divider()

# --- ФУНКЦИЯ ЗА ПОКАЗВАНЕ НА СРЕЩА ---
def render_match_report(m):
    # Визуална карта на срещата
    with st.container():
        st.markdown(f"""
        <div class="match-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 18px; font-weight: bold;">🏟️ {m['match']}</span>
                <span style="color: #00ff88; font-weight: bold; font-size: 20px;">{m['prob']}</span>
            </div>
            <div style="color: #888; font-size: 14px; margin-top: 5px;">🎯 {m['market']}: <b>{m['tip']}</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Разгъващ се панел с пълномащабен анализ
        with st.expander("📊 КЛИКНИ ЗА ПЪЛЕН ПОДРОБЕН АНАЛИЗ"):
            st.markdown("<div class='analysis-block'>", unsafe_allow_html=True)
            
            # 1. СТРАТЕГИЧЕСКИ АНАЛИЗ
            st.markdown("#### 🔍 1. Пълномащабен тактически анализ")
            st.write(m['strat'])
            
            st.divider()
            
            # 2. ДАННИ ЗА ИГРАЧИ И КОНТУЗИИ
            st.markdown("#### 🚑 2. Кадрова ситуация и новини")
            st.info(m['injuries'])
            
            st.divider()
            
            # 3. СЪДИЯ И ПСИХОЛОГИЯ
            st.markdown("#### ⚖️ 3. Съдийски фактор и дисциплина")
            st.write(m['ref'])
            
            st.divider()
            
            # 4. ДОПЪЛНИТЕЛНИ ПАЗАРИ (КРАСИВ ИЗГЛЕД)
            st.markdown("#### 📈 4. Вероятности за други пазари")
            for market, chance in m['other_markets'].items():
                st.markdown(f"""
                <div class="stat-row">
                    <span>{market}</span>
                    <span style="color: #00ff88;">{chance}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    st.write("") # Разстояние между картите

# --- ДАННИ ЗА 5-ТЕ СРЕЩИ ---
# Тук са твоите 5 мача с техните мащабни анализи
matches_data = [
    {
        "match": "Arsenal vs Manchester United",
        "market": "Корнери - Азиатски Хендикап",
        "tip": "Арсенал -2.5",
        "prob": "89%",
        "strat": "Пълномащабният анализ на интернет пространството и тактическите бордове показва, че Арсенал доминира фланговете с 72% владеене в последната третина. United ще използват нисък блок, което генерира средно 8.5 корнера за противника при гостувания.",
        "injuries": "United са без двамата си основни централни защитници, което води до панически чистения в аут. Арсенал излиза с пълен състав в атака.",
        "ref": "Майкъл Оливър позволява твърда игра на крилата, което увеличава шанса за блокирани центрирания и корнери.",
        "other_markets": {"Над 2.5 гола": "74%", "Победа Арсенал": "68%", "Картони Над 3.5": "51%"}
    },
    {
        "match": "Inter vs Juventus",
        "market": "Общо Картони",
        "tip": "Над 5.5 картона",
        "prob": "94%",
        "strat": "Derby d'Italia е мачът с най-висок интензитет на фаулове в Италия. Анализът на социалните мрежи показва огромно напрежение в лагера на Ювентус, а Интер ще пресира агресивно в центъра.",
        "injuries": "Липсата на дисциплиниран дефанзивен халф при Юве ще доведе до принудителни тактически нарушения.",
        "ref": "Давиде Маса показва средно 5.8 картона в големи дербита.",
        "other_markets": {"Червен картон": "40%", "Под 2.5 гола": "82%", "Равен": "35%"}
    },
    # Добави още 3 срещи по същия модел тук...
]

# Извеждане на 5-те мача
for m in matches_data:
    render_match_report(m)

# --- АРХИВ ---
st.header("📂 Архив")
st.write("Последни резултати от AI анализа...")
# (Кодът за архива тук)
