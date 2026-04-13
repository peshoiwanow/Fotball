import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА СКРАПЕРА (Compatibility Mode)...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва GEMINI_API_KEY!")
        return

    # Използваме директен v1 път към gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt = (
        f"Днес е {today}. Намери 5 футболни мача за днес. "
        "Върни САМО чист JSON списък: "
        "[{\"match\": \"...\", \"tip\": \"...\", \"prob\": \"...\"}]"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        res_data = response.json()
        
        # Ако v1 даде 404, опитваме последен шанс с v1beta автоматично
        if response.status_code == 404:
            print("🔄 v1 не е намерен, опит с v1beta...")
            url = url.replace("/v1/", "/v1beta/")
            response = requests.post(url, json=payload, timeout=30)
            res_data = response.json()

        if 'error' in res_data:
            print(f"❌ API ГРЕШКА ({res_data['error'].get('status')}): {res_data['error'].get('message')}")
            return

        raw_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Почистване на JSON ако AI сложи markdown
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
