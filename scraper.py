import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОНОМНИЯ AI СКРАПЕР (Direct API Mode)...")
    if not GEMINI_API_KEY:
        print("❌ Липсва API Ключ!")
        return

    # URL за директен достъп до стабилната версия v1
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt_text = f"Днес е {today}. Намери 5-те най-важни футболни мача за днес или утре. Върни резултата САМО като чист JSON списък от обекти с ключове: match, prob, strat, tip, market, injuries, ref."

    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        print("🔍 Директно запитване към Google AI...")
        response = requests.post(url, json=payload, timeout=30)
        res_data = response.json()
        
        # Извличане на текста от отговора на Google
        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Изчистване на JSON формата
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        final_json = json.loads(raw_text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_json, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Записани {len(final_json)} мача.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")
        if 'res_data' in locals():
            print(f"DEBUG: {res_data}")

if __name__ == "__main__":
    run()
