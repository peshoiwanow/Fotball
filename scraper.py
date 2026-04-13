import json
import os
import requests
import time
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def fetch_data():
    today = datetime.now().strftime('%d.%m.%Y')
    
    # Използваме доказано работещия модел и версии
    model_name = "models/gemini-2.5-flash"
    # Опитваме първо с v1beta, после с v1
    api_versions = ["v1beta", "v1"]
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5 реални футболни мача за днес. "
        "Върни резултата САМО като чист JSON списък със следните ключове: "
        "match, strat, injuries, ref, tip, prob."
    )

    for version in api_versions:
        url = f"https://generativelanguage.googleapis.com/{version}/{model_name}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.1}
        }

        try:
            print(f"📡 Опит с {version} и {model_name}...")
            response = requests.post(url, json=payload, timeout=120)
            res_data = response.json()

            if 'error' in res_data:
                print(f"⚠️ Грешка в {version}: {res_data['error']['message']}")
                continue

            raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Почистване на JSON
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0]
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0]
            
            return json.loads(raw_text.strip())

        except Exception as e:
            print(f"❌ Техническа грешка: {e}")
            time.sleep(5)
            
    return None

def run():
    print("🚀 СТАРТ НА СИНХРОНИЗИРАНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY: return
    
    result = fetch_data()
    if result:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! Данните са в data.json.")
    else:
        print("💀 Неуспешно свързване с API.")

if __name__ == "__main__":
    run()
