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

    # Изрично конфигуриране за работа със стабилната версия v1
    genai.configure(api_key=GEMINI_API_KEY, transport='rest')
    
    # Използваме базовото име на модела
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    today = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    Днес е {today}. Намери 5-те най-важни футболни мача за днес или утре.
    Върни резултата САМО като чист JSON списък, без никакви обяснения преди или след него:
    [
      {{
        "match": "Отбор А - Отбор Б",
        "prob": "Лига и Час",
        "strat": "Подробен анализ...",
        "tip": "Прогноза",
        "market": "Коефициент",
        "injuries": "Контузии",
        "ref": "Съдия"
      }}
    ]
    """

    try:
        print("🔍 AI претърсва интернет за мачове...")
        # Генериране на съдържание
        response = model.generate_content(prompt)
        
        # Почистване на текста от евентуални markdown маркери
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        data = json.loads(content.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ: Записани {len(data)} мача.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")

if __name__ == "__main__":
    run()
