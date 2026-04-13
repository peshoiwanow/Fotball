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
    # Използваме v1beta за стабилен достъп до Google Search
    model_path = "models/gemini-2.5-flash"
    
    # Оптимизиран промпт за подробни анализи
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да направиш ДЪЛБОК анализ на 3 топ футболни мача за днес. "
        "За ВСЕКИ мач попълни тези полета с МНОГО детайли (поне 3-4 изречения за секция): "
        "1. match: име на мача. "
        "2. strat: подробна тактическа обосновака и форма на отборите. "
        "3. injuries: списък с ключови контузени и наказани играчи. "
        "4. ref: име на съдията и какъв е стилът му на свирене. "
        "5. tip: конкретна прогноза с аргументация. "
        "6. prob: процентна вероятност за успех и очакван коефициент. "
        "Върни резултата САМО като чист JSON списък. Не оставяй полета с 'N/A'!"
    )

    for api_key in KEYS:
        if not api_key: continue
            
        url = f"https://generativelanguage.googleapis.com/v1beta/{model_path}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": {"temperature": 0.2} # Леко вдигаме температурата за по-креативен текст
        }

        for attempt in range(3):
            try:
                print(f"📡 Опит с ключ (начало: {api_key[:5]})...")
                response = requests.post(url, json=payload, timeout=120)
                res_data = response.json()

                if 'error' in res_data:
                    msg = res_data['error']['message']
                    print(f"⚠️ Грешка: {msg}")
                    if "quota" in msg.lower() or "limit" in msg.lower():
                        break 
                    if "high demand" in msg.lower():
                        time.sleep(30)
                        continue
                    break

                # Извличане и почистване на JSON
                raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0]
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0]
                
                data = json.loads(raw_text.strip())
                
                # Проверка за липсващи ключове (защита срещу KeyError)
                required_keys = ["match", "strat", "injuries", "ref", "tip", "prob"]
                for item in data:
                    for key in required_keys:
                        if key not in item or not item[key] or item[key] == "N/A":
                            item[key] = "В процес на събиране на детайлни данни..."
                
                return data

            except Exception as e:
                print(f"❌ Грешка: {e}")
                time.sleep(10)
            
    return None

def run():
    print("🚀 СТАРТ НА ПОДРОБНИЯ СКРАПЕР...")
    result = fetch_data()
    
    if result:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: data.json е обновен с пълни анализи за {len(result)} мача.")
    else:
        print("💀 Неуспех. Моля, проверете логовете за натоварване.")

if __name__ == "__main__":
    run()
