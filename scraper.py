import json
import os
import google.generativeai as genai
from datetime import datetime

# Ключ за Gemini от твоите Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА АВТОНОМНИЯ AI СКРАПЕР...")
    
    if not GEMINI_API_KEY:
        print("❌ Липсва API Ключ!")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    # Използваме модела за търсене на информация в реално време
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    today = datetime.now().strftime('%d.%m.%Y')
    
    # AI инструкция: Намери мачовете сам
    prompt = f"""
    Днес е {today}. Използвай Google Search и намери 5-те най-интересни футболни мача за днес или утре от големите европейски лиги.
    За всеки мач направи:
    1. Пълен анализ на формата и тактиката.
    2. Потвърдени състави и контузени.
    3. Информация за съдията.
    4. Точна прогноза и коефициент.

    Върни резултата САМО като чист JSON списък в този формат:
    [
      {{
        "match": "Отбор А - Отбор Б",
        "prob": "Лига и Час",
        "strat": "Много подробен анализ (поне 10 изречения)...",
        "tip": "Прогноза",
        "market": "Коефициент",
        "injuries": "Състави и контузии",
        "ref": "Информация за съдията"
      }}
    ]
    """

    try:
        print("🔍 AI претърсва интернет за мачове...")
        response = model.generate_content(prompt)
        
        # Почистване на отговора
        text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(text)
        
        if data:
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ УСПЕХ: Намерени и анализирани {len(data)} мача чрез AI Search!")
        else:
            print("⚠️ AI не върна данни.")
            
    except Exception as e:
        print(f"❌ Критична грешка: {e}")

if __name__ == "__main__":
    run()
