import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА СКРАПЕРА (Universal Mode)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва GEMINI_API_KEY!")
        return

    # Използваме базовия gemini-pro през v1 - това е най-стабилният път
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt_text = (
        f"Днес е {today}. Намери 5 интересни футболни мача за днес или утре. "
        "Направи кратък анализ и прогноза. "
        "Върни резултата САМО като чист JSON списък: "
        "[{\"match\": \"...\", \"prob\": \"...\", \"strat\": \"...\", \"tip\": \"...\", \"market\": \"...\", \"injuries\": \"...\", \"ref\": \"...\"}]"
    )

    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}

    try:
        response = requests.post(url, json=payload, timeout=30)
        res_data = response.json()
        
        # Ако пак има грешка, тук ще я видим ясно
        if 'error' in res_data:
            print(f"❌ API Грешка: {res_data['error']['message']}")
            return

        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Чистене на излишни знаци
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        final_data = json.loads(raw_text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Записани {len(final_data)} мача.")
            
    except Exception as e:
        print(f"❌ Грешка при обработка: {str(e)}")

if __name__ == "__main__":
    run()
