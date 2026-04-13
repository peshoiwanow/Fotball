import json
import os
import requests
import time
from datetime import datetime

# Вземаме API ключа от GitHub Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_data():
    # Модели, които ще опитаме последователно
    models_to_try = ["models/gemini-2.5-flash", "models/gemini-1.5-flash"]
    today = datetime.now().strftime('%d.%m.%Y')
    
    # Промпт с точните ключове за твоя Streamlit сайт
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5 реални футболни мача за {today}. "
        "За всеки мач направи детайлен анализ. "
        "Върни резултата САМО като чист JSON списък със следните ключове: "
        "match (име на мача), strat (експертна обосновка), injuries (състави и контузии), "
        "ref (съдия и дисциплина), tip (прогноза), prob (коефициент/вероятност)."
    )

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}], # Активираме търсенето
            "generationConfig": {
                "temperature": 0.1 # Висока точност
            }
        }

        # Опитваме до 3 пъти при претоварване (High Demand)
        for attempt in range(3):
            try:
                print(f"📡 Опит {attempt+1} с модел {model}...")
                response = requests.post(url, json=payload, timeout=180)
                res_data = response.json()

                if 'error' in res_data:
                    error_msg = res_data['error']['message']
                    print(f"⚠️ Грешка от Google: {error_msg}")
                    if "high demand" in error_msg.lower():
                        time.sleep(20) # Изчакваме при натоварване
                        continue
                    break

                # Извличане и изчистване на JSON текста
                raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0]
                
                return json.loads(raw_text.strip())

            except Exception as e:
                print(f"❌ Грешка при опит: {e}")
                time.sleep(5)
    
    return None

def run():
    print("🚀 СТАРТ НА АВТОМАТИЗИРАНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ в Secrets!")
        return

    result = fetch_data()
    
    if result:
        # Записваме данните в data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! Записани са {len(result)} мача.")
    else:
        print("💀 Всички опити се провалиха.")

if __name__ == "__main__":
    run()
