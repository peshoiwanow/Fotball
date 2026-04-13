import json
import os
import requests
from datetime import datetime

# Вземаме ключа от GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОМАТИЗИРАНИЯ СКРАПЕР...")
    
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: GEMINI_API_KEY не е намерен в Secrets!")
        return

    # Динамично вземане на днешната дата
    today = datetime.now().strftime('%d.%m.%Y')
    
    # Конфигурация на модела и API адреса
    selected_model = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
    
    # Промпт за глобално търсене на мачове само за днес
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача, "
        f"които се играят ЕДИНСТВЕНО НА {today}. "
        "Включи мачове от всякакви професионални лиги по света (не само топ първенствата). "
        "За всеки мач дай анализ и прогноза. "
        "Върни резултата САМО като чист JSON списък от обекти с ключове: "
        "match, prob, strat, tip, market, injuries, ref. Не пиши никакъв друг текст!"
    )

    # Payload с активиран Google Search инструмент
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}], 
        "generationConfig": {
            "temperature": 0.1  # Ниска температура за фактическа точност
        }
    }

    try:
        print(f"📡 Търсене в реално време за мачове на дата: {today}...")
        response = requests.post(url, json=payload, timeout=120)
        res_data = response.json()

        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        # Извличане на текста от отговора
        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Почистване на JSON от евентуални Markdown тагове
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        # Валидиране и запис на данните
        data = json.loads(raw_text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ УСПЕХ: {len(data)} актуални мача за {today} бяха записани в data.json!")

    except Exception as e:
        print(f"❌ КРИТИЧНА ГРЕШКА: {str(e)}")

if __name__ == "__main__":
    run()
