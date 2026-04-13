import json
import os
import requests
import time
from datetime import datetime

# Вземаме ключа от GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_data():
    today = datetime.now().strftime('%d.%m.%Y')
    # Използваме v1beta за поддръжка на Google Search
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Промптът е стриктно форматиран, за да съвпадне с твоя app.py
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача, "
        f"които се играят ДНЕС ({today}). Включи разнообразни лиги (не само топ 5). "
        "Върни резултата ЕДИНСТВЕНО като чист JSON списък от обекти с тези ключове: "
        "match, strat, injuries, ref, tip, prob. Не добавяй никакъв друг текст!"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}], # Активираме търсенето в реално време
        "generationConfig": {"temperature": 0.1}
    }

    # Логика за повторни опити при натоварване
    for attempt in range(5):
        try:
            print(f"📡 Опит {attempt+1}: Търсене на мачове за {today}...")
            response = requests.post(url, json=payload, timeout=120)
            res_data = response.json()

            if 'error' in res_data:
                msg = res_data['error']['message']
                print(f"⚠️ API съобщение: {msg}")
                if "high demand" in msg.lower():
                    time.sleep(20) # Изчакване при претоварване
                    continue
                break

            # Извличане на текста и почистване от Markdown
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0]
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0]
            
            return json.loads(raw_text.strip())

        except Exception as e:
            print(f"❌ Грешка при изпълнението: {e}")
            time.sleep(10)
            
    return None

def run():
    print("🚀 СТАРТ НА АВТОМАТИЗИРАНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY:
        print("❌ КРИТИЧНА ГРЕШКА: Липсва GEMINI_API_KEY!")
        return
    
    result = fetch_data()
    if result:
        # Записваме данните в data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: data.json е обновен с {len(result)} мача!")
    else:
        print("💀 Скриптът не успя да извлече данни след всички опити.")

if __name__ == "__main__":
    run()
