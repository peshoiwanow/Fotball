import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА ЖИВИЯ СКРАПЕР (Final Version)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ!")
        return

    # Използваме работещия модел gemini-2.5-flash
    selected_model = "models/gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    
    # Промптът е максимално ясен, за да получим чист списък
    prompt = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5 истински футболни мача за днес или утре. "
        "Върни резултата САМО като чист JSON списък от обекти с ключове: "
        "match, prob, strat, tip, market, injuries, ref. Не пиши нищо друго!"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}], 
        "generationConfig": {
            "temperature": 0.1  # Максимална точност за фактите
            # ПРЕМАХНАТО: responseMimeType, за да не гърми
        }
    }

    try:
        print(f"📡 Търсене на реални мачове за {today}...")
        response = requests.post(url, json=payload, timeout=120)
        res_data = response.json()

        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        # Вземаме суровия текст от AI
        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Почистване на текста от markdown символи (```json ... ```)
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        data = json.loads(raw_text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"✅ УСПЕХ: Записани са {len(data)} актуални мача в data.json!")

    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")
        if 'raw_text' in locals():
            print(f"DEBUG (Суров текст): {raw_text[:100]}...")

if __name__ == "__main__":
    run()
