import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА СКРАПЕРА (Direct Mode)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ в Secrets!")
        return

    # Използваме v1beta адреса, за да избегнем 404 грешката
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt_text = (
        f"Днес е {today}. Използвай Google Search, за да намериш 5-те най-интересни футболни мача за днес или утре. "
        "Направи подробен анализ, състави, информация за съдията и дай прогноза с коефициент. "
        "Върни резултата САМО като чист JSON списък: "
        "[{\"match\": \"...\", \"prob\": \"...\", \"strat\": \"...\", \"tip\": \"...\", \"market\": \"...\", \"injuries\": \"...\", \"ref\": \"...\"}]"
    )

    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}

    try:
        print("🔍 AI анализира и претърсва интернет...")
        response = requests.post(url, json=payload, timeout=40)
        res_data = response.json()
        
        if 'candidates' not in res_data:
            print(f"❌ Грешка от API: {res_data}")
            return

        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Почистване на JSON формата от AI маркери
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0]
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0]
            
        data = json.loads(raw_text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Анализирани {len(data)} мача.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")

if __name__ == "__main__":
    run()
