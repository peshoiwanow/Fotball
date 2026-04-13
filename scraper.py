import json
import os
import requests
import time
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_data():
    # Пробваме първо с 2.5, ако не стане - с 1.5
    models_to_try = ["models/gemini-2.5-flash", "models/gemini-1.5-flash"]
    today = datetime.now().strftime('%d.%m.%Y')
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача за {today}. "
        "Включи мачове от всякакви лиги. Върни САМО чист JSON списък с ключове: "
        "match, prob, strat, tip, market, injuries, ref."
    )

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.1}
        }

        # Опитваме 3 пъти за всеки модел
        for attempt in range(3):
            try:
                print(f"📡 Опит {attempt+1} с модел {model}...")
                response = requests.post(url, json=payload, timeout=180) # Увеличен timeout
                res_data = response.json()

                if 'error' in res_data:
                    error_msg = res_data['error']['message']
                    print(f"⚠️ Грешка от Google: {error_msg}")
                    if "high demand" in error_msg.lower():
                        print("⏳ Сървърът е зает, чакаме 30 сек...")
                        time.sleep(30)
                        continue
                    break # Ако е друга грешка, не опитваме пак с този модел

                raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0]
                
                return json.loads(raw_text.strip())

            except Exception as e:
                print(f"❌ Грешка при опит: {e}")
                time.sleep(10)
    
    return None

def run():
    print("🚀 СТАРТ НА БРОНИРАНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY:
        return

    result = fetch_data()
    if result:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("✅ УСПЕХ! Данните са записани.")
    else:
        print("💀 Всички опити се провалиха поради натоварване на сървърите.")

if __name__ == "__main__":
    run()
