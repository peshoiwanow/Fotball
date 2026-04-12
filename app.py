def render_match(m):
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

    with st.expander("📄 ВИЖ ПЪЛЕН ЕКСПЕРТЕН АНАЛИЗ"):
        st.markdown("<div class='section-header'>🔍 1. Пълна Обосновка и Тактика</div>", unsafe_allow_html=True)
        # Използваме st.write вместо st.markdown за strat, за да избегнем грешно форматиране
        st.write(m.get('strat', 'Анализът се обработва...'))
        
        st.markdown("<div class='section-header'>🚑 2. Кадрова Ситуация (Контузени и Наказани)</div>", unsafe_allow_html=True)
        # Слагаме ярък фон, за да се чете лесно
        st.warning(m.get('injuries', 'Няма критични новини.'))
        
        st.markdown("<div class='section-header'>⚖️ 3. Рефер и Психология</div>", unsafe_allow_html=True)
        st.write(m.get('ref', 'Информацията се обновява.'))
