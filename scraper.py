import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА ЖИВИЯ СКРАПЕР (Google Search Fixed)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ!")
        return

    # Използваме потвърдения работещ модел
    selected_model = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5 истински футболни мача за днес или утре. "
        "Върни резултата САМО като чист JSON списък от обекти с ключове: "
        "match, prob, strat, tip, market, injuries, ref."
    )

    # Поправка на инструмента според лога: google_search вместо google_search_retrieval
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}], 
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    try:
        print(f"📡 Търсене в реално време за мачове на {today}...")
        response = requests.post(url, json=payload, timeout=120)
        res_data = response.json()

        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
        data = json.loads(raw_text)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ УСПЕХ: Намерени и записани {len(data)} реални мача!")

    except Exception as e:
        print(f"❌ Грешка при обработка: {str(e)}")

if __name__ == "__main__":
    run()
