import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОМАТИЗИРАНИЯ СКРАПЕР...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ!")
        return

    today = datetime.now().strftime('%d.%m.%Y')
    
    # Можеш да пробваш с 1.5-flash, ако 2.5-flash е претоварен
    selected_model = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш точно 5 реални футболни мача, "
        f"които се играят ЕДИНСТВЕНО НА {today}. "
        "Включи мачове от всякакви професионални лиги по света (не само топ първенствата). "
        "Върни резултата САМО като чист JSON списък от обекти с ключове: "
        "match, prob, strat, tip, market, injuries, ref. Не пиши нищо друго!"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}], 
        "generationConfig": {"temperature": 0.1}
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        res_data = response.json()

        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        data = json.loads(raw_text.strip())
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ УСПЕХ: Записани мачове за {today}!")

    except Exception as e:
        print(f"❌ Грешка: {str(e)}")

if __name__ == "__main__":
    run()
