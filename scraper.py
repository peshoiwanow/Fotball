import json
import os
import requests
import time
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_data():
    # Поправени имена на моделите за v1beta
    models_to_try = ["models/gemini-2.0-flash-exp", "models/gemini-1.5-flash"]
    today = datetime.now().strftime('%d.%m.%Y')
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача за {today}. "
        "За всеки мач направи детайлен анализ. "
        "Върни резултата САМО като чист JSON списък със следните ключове: "
        "match (име на мача), strat (експертна обосновка), injuries (състави и контузии), "
        "ref (съдия и дисциплина), tip (прогноза), prob (коефициент/вероятност)."
    )

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.1}
        }

        for attempt in range(3):
            try:
                print(f"📡 Опит {attempt+1} с модел {model}...")
                response = requests.post(url, json=payload, timeout=120)
                res_data = response.json()

                if 'error' in res_data:
                    error_msg = res_data['error']['message']
                    print(f"⚠️ Грешка: {error_msg}")
                    if "high demand" in error_msg.lower():
                        time.sleep(15)
                        continue
                    break # Преминаваме на следващия модел при друга грешка

                raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0]
                
                return json.loads(raw_text.strip())
            except Exception as e:
                print(f"❌ Грешка: {e}")
                time.sleep(5)
    return None

def run():
    print("🚀 СТАРТ НА ФИНАЛНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY: return
    
    result = fetch_data()
    if result:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! Записани са {len(result)} мача.")
    else:
        print("💀 Всички модели са претоварени в момента.")

if __name__ == "__main__":
    run()
