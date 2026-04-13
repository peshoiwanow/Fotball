import json
import os
import requests
import time
from datetime import datetime

# Списък с ключове от Secrets
KEYS = [
    os.getenv("GEMINI_API_KEY"),
    os.getenv("GEMINI_API_KEY_2")
]

def fetch_data():
    today = datetime.now().strftime('%d.%m.%Y')
    # Използваме v1beta за Google Search функционалност
    model_path = "models/gemini-2.5-flash"
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача за {today}. "
        "Върни резултата САМО като чист JSON списък със следните ключове: "
        "match, strat, injuries, ref, tip, prob. Не пиши нищо друго!"
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

        try:
            print(f"📡 Опит с API ключ (започващ с {api_key[:5]})...")
            response = requests.post(url, json=payload, timeout=120)
            res_data = response.json()

            if 'error' in res_data:
                msg = res_data['error']['message']
                print(f"⚠️ Грешка: {msg}")
                # Ако квотата е свършила, премини на следващия ключ
                if "quota" in msg.lower() or "limit" in msg.lower():
                    print("🔄 Квотата е изчерпана. Превключвам на следващия ключ...")
                    continue
                # Ако сървърът е претоварен, изчакай малко
                if "high demand" in msg.lower():
                    print("⏳ Високо натоварване. Чакам 20 сек...")
                    time.sleep(20)
                    continue
                continue

            # Обработка на резултата
            raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0]
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0]
            
            data = json.loads(raw_text.strip())
            
            # Защита срещу KeyError за Streamlit сайта
            for item in data:
                for key in ["match", "strat", "injuries", "ref", "tip", "prob"]:
                    if key not in item:
                        item[key] = "N/A"
            
            return data

        except Exception as e:
            print(f"❌ Техническа грешка: {e}")
            continue
            
    return None

def run():
    print("🚀 СТАРТ НА СКРАПЕР С ДВОЙНА КВОТА...")
    result = fetch_data()
    
    if result:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: data.json е обновен с {len(result)} мача!")
    else:
        print("💀 Всички ключове/опити се провалиха.")

if __name__ == "__main__":
    run()
