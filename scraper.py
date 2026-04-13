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

    # НОВИЯТ URL формат за Gemini 1.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt_text = f"Днес е {today}. Намери 5-те най-интересни футболни мача за днес или утре. Върни резултата САМО като чист JSON списък: [{{'match': '...', 'prob': '...', 'strat': '...', 'tip': '...', 'market': '...', 'injuries': '...', 'ref': '...'}}]"

    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    try:
        print("🔍 Запитване към Google AI...")
        response = requests.post(url, json=payload, timeout=30)
        res_data = response.json()
        
        # Проверка за грешки в отговора
        if 'error' in res_data:
            print(f"❌ Грешка от Google: {res_data['error']['message']}")
            return

        # Извличане на текста
        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Премахване на markdown ако има такъв
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

if __name__ == "__main__":
    run()
