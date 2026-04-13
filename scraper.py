import json
import os
import requests
import time
from datetime import datetime

# Вземаме и двата ключа от GitHub Secrets
KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2")
]

def fetch_data():
    today = datetime.now().strftime('%d.%m.%Y')
    # Използваме v1beta за поддръжка на инструменти като Google Search
    model_path = "models/gemini-2.5-flash"
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача за {today}. "
        "Върни резултата САМО като чист JSON списък от обекти със следните ключове: "
        "match, strat, injuries, ref, tip, prob. Не добавяй никакъв друг текст!"
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

        # Опити за справяне с натоварването
        for attempt in range(3):
            try:
                print(f"📡 Опит с ключ (започващ с {api_key[:5]})...")
                response = requests.post(url, json=payload, timeout=120)
                res_data = response.json()

                if 'error' in res_data:
                    msg = res_data['error']['message']
                    print(f"⚠️ Грешка: {msg}")
                    # Ако квотата е изчерпана, премини на следващия ключ
                    if "quota" in msg.lower() or "limit" in msg.lower():
                        break 
                    # Ако натоварването е голямо, изчакай малко
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
                
                # ГАРАНЦИЯ СРЕЩУ KeyError: Проверяваме за всички необходими ключове
                required_keys = ["match", "strat", "injuries", "ref", "tip", "prob"]
                for item in data:
                    for key in required_keys:
                        if key not in item or not item[key]:
                            item[key] = "Няма налична информация"
                
                return data

            except Exception as e:
                print(f"❌ Техническа грешка: {e}")
                time.sleep(10)
            
    return None

def run():
    print("🚀 СТАРТ НА СКРАПЕР С ДВОЙНА КВОТА...")
    result = fetch_data()
    
    if result:
        # Записваме данните в data.json за обновяване на сайта
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: data.json е обновен с {len(result)} мача!")
    else:
        print("💀 Всички ключове и опити се провалиха.")

if __name__ == "__main__":
    run()
