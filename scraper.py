import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА ЖИВИЯ СКРАПЕР (Google Search Mode)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ!")
        return

    # Използваме вече потвърдения работещ модел
    selected_model = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    
    # По-прецизен промпт за актуални данни
    prompt = (
        f"Днес е {today}. ИЗПОЛЗВАЙ GOOGLE SEARCH, за да намериш 5 реални футболни мача, "
        "които ще се играят днес или утре в Европа (висшите лиги). "
        "За всеки мач дай: отбори, вероятност за победа, стратегия, съвет за залог, "
        "пазар, контузени играчи и съдия. "
        "Върни резултата САМО като чист JSON списък."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search_retrieval": {}}], # ТОВА ВКЛЮЧВА ЖИВОТО ТЪРСЕНЕ
        "generationConfig": {
            "temperature": 0.2, # По-ниска температура за по-голяма точност
            "responseMimeType": "application/json"
        }
    }

    try:
        print(f"📡 Търсене в реално време за мачове на {today}...")
        response = requests.post(url, json=payload, timeout=120) # Увеличено време за търсене
        res_data = response.json()

        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
        data = json.loads(raw_text)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ УСПЕХ: Намерени и анализирани {len(data)} РЕАЛНИ мача!")

    except Exception as e:
        print(f"❌ Грешка: {str(e)}")

if __name__ == "__main__":
    run()
