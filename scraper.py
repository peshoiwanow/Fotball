import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОНОМНИЯ AI СКРАПЕР...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва GEMINI_API_KEY!")
        return

    # Използваме стабилния v1 адрес с новия ти ключ
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt = (
        f"Днес е {today}. Намери 5-те най-интересни футболни мача за днес или утре. "
        "Направи подробен анализ, прогноза и състави. "
        "Върни резултата САМО като чист JSON списък от обекти с ключове: "
        "match, prob, strat, tip, market, injuries, ref."
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }

    try:
        print("🔍 AI анализира футболни срещи...")
        response = requests.post(url, json=payload, timeout=60)
        res_data = response.json()
        
        if 'error' in res_data:
            print(f"❌ API ГРЕШКА: {res_data['error']['message']}")
            return

        # Извличане на готовия JSON от AI
        raw_text = res_data['candidates'][0]['content']['parts'][0]['text']
        data = json.loads(raw_text)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Записани {len(data)} мача в data.json")
            
    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")

if __name__ == "__main__":
    run()
