import json
import os
import requests
import time
from datetime import datetime

# Вземаме двата ключа от GitHub Secrets
KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2")
]

def fetch_data():
    today = datetime.now().strftime('%d.%m.%Y')
    # Използваме v1beta за работа с Google Search
    model_path = "models/gemini-2.5-flash"
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5 реални футболни мача за {today}. "
        "Върни резултата САМО като чист JSON списък със следните ключове на английски: "
        "match, strat, injuries, ref, tip, prob."
    )

    for api_key in KEYS:
        if not api_key:
            continue
            
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.1}
        }

        # Опитваме до 3 пъти при високо натоварване
        for attempt in range(3):
            try:
                print(f"📡 Опит с ключ (начало: {api_key[:5]})...")
                response = requests.post(url, json=payload, timeout=120)
                res_data = response.json()

                if 'error' in res_data:
                    msg = res_data['error']['message']
                    print(f"⚠️ Грешка: {msg}")
                    # Ако квотата е свършила, премини на следващия ключ
                    if "quota" in msg.lower() or "limit" in msg.lower():
                        break 
                    # Ако натоварването е голямо, изчакай и опитай пак
                    if "high demand" in msg.lower():
                        time.sleep(20)
                        continue
                    break

                # Извличане и изчистване на JSON текста
                raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0]
                
                data = json.loads(raw_text.strip())
                
                # ГАРАНЦИЯ: Проверяваме за всички ключове, за да спрем KeyError
                required_keys = ["match", "strat", "injuries", "ref", "tip", "prob"]
                for item in data:
                    for key in required_keys:
                        if key not in item:
                            item[key] = "Няма информация"
                
                return data

            except Exception as e:
                print(f"❌ Грешка: {e}")
                time.sleep(5)
            
    return None

def run():
    print("🚀 СТАРТ НА СКРАПЕР С ДВОЙНА КВОТА...")
    result = fetch_data()
    
    if result:
        # Записваме в data.json, което GitHub Action ще качи
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! Записани са {len(result)} мача.")
    else:
        print("💀 Всички ключове и опити се провалиха.")

if __name__ == "__main__":
    run()
