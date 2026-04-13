import json
import os
import requests
import time
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_data():
    today = datetime.now().strftime('%d.%m.%Y')
    # Използваме само v1beta, защото там 'tools' е поддържан
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5 реални футболни мача, които се играят днес. "
        "Включи лиги от цял свят. Върни резултата САМО като чист JSON списък със следните ключове: "
        "match, strat, injuries, ref, tip, prob. Не добавяй обяснения извън JSON."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.1}
    }

    # Правим до 5 опита с прогресивно изчакване
    for attempt in range(5):
        try:
            print(f"📡 Опит {attempt+1} за извличане на мачове...")
            response = requests.post(url, json=payload, timeout=120)
            res_data = response.json()

            if 'error' in res_data:
                msg = res_data['error']['message']
                print(f"⚠️ Google API съобщение: {msg}")
                if "high demand" in msg.lower():
                    wait_time = (attempt + 1) * 20 # Увеличаваме времето за чакане
                    print(f"⏳ Сървърите са заети. Чакаме {wait_time} секунди...")
                    time.sleep(wait_time)
                    continue
                return None

            # Валидиране на отговора
            if 'candidates' in res_data:
                raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                # Почистване на JSON тагове
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0]
                
                return json.loads(raw_text.strip())

        except Exception as e:
            print(f"❌ Грешка: {e}")
            time.sleep(10)
            
    return None

def run():
    print("🚀 СТАРТ НА АВТОМАТИЗИРАНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY: return
    
    result = fetch_data()
    if result:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: data.json е обновен с {len(result)} мача!")
    else:
        print("💀 Неуспех след всички опити. Опитай ръчно след малко.")

if __name__ == "__main__":
    run()
