import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОНОМНИЯ AI СКРАПЕР (Stable Mode)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва GEMINI_API_KEY!")
        return

    # Използваме базовия gemini-pro през v1beta - това е най-универсалният модел
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt = (
        f"Днес е {today}. Намери 5-те най-интересни футболни мача за днес или утре. "
        "Направи анализ и прогноза. "
        "Върни резултата САМО като чист JSON списък от обекти с ключове: "
        "match, prob, strat, tip, market, injuries, ref."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        print("🔍 Комуникация със стабилния модел на Google...")
        response = requests.post(url, json=payload, timeout=60)
        res_data = response.json()
        
        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        # Извличане на текста и почистване на JSON
        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        data = json.loads(raw_text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Записани {len(data)} мача.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")
        if 'res_data' in locals():
            print(f"DEBUG: {res_data}")

if __name__ == "__main__":
    run()
