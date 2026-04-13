import json
import os
import google.generativeai as genai
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОНОМНИЯ AI СКРАПЕР...")
    if not GEMINI_API_KEY:
        print("❌ Липсва API Ключ!")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    # ФИКС: Използваме стабилното име на модела
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    Днес е {today}. Намери 5-те най-важни футболни мача за днес или утре.
    Върни резултата САМО като чист JSON списък:
    [
      {{
        "match": "Отбор А - Отбор Б",
        "prob": "Лига и Час",
        "strat": "Подробен анализ на форма и тактика...",
        "tip": "Прогноза",
        "market": "Коефициент",
        "injuries": "Контузии и състави",
        "ref": "Съдия"
      }}
    ]
    """

    try:
        print("🔍 AI претърсва интернет за мачове...")
        # Добавяме и сигурен timeout
        response = model.generate_content(prompt)
        
        text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(text)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Записани {len(data)} мача.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {e}")

if __name__ == "__main__":
    run()
