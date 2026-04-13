import json
import os
import time
from datetime import datetime
import google.generativeai as genai

# Конфигурация на AI
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def run():
    print("🌐 AI стартира сканиране на интернет пространството...")
    
    # Използваме модела за търсене в реално време
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = """
    Действай като професионален футболен анализатор и скаут. 
    Изпълни следните стъпки:
    1. Провери програмата за днес (13.04.2026) във водещи сайтове като Flashscore и SofaScore.
    2. Избери 5-те мача с най-висока статистическа вероятност за успех (базирано на форма и преки двубои).
    3. За ВСЕКИ от тези 5 мача намери:
       - Пълни състави и липсващи ключови играчи (контузии/наказания).
       - Кой е съдията и каква е неговата средна статистика за картони.
       - Последни новини около лагерите на отборите.
    4. Направи масивен анализ от поне 10 изречения за всеки мач, обяснявайки ЗАЩО избираш точно тази прогноза.
    
    Върни резултата ЕДИНСТВЕНО като JSON списък в този формат (строго спазвай структурата):
    [
      {
        "match": "Отбор А - Отбор Б",
        "prob": "Лига и Час",
        "strat": "ПЪЛЕН ПОДРОБЕН АНАЛИЗ ТУК (поне 10 изречения)",
        "tip": "Конкретна прогноза и Коефициент",
        "market": "Коефициент",
        "injuries": "ПОДРОБНИ СЪСТАВИ И ЛИПСВАЩИ ИГРАЧИ",
        "ref": "ИНФОРМАЦИЯ ЗА СЪДИЯТА",
        "other": {"Time": "Час"}
      }
    ]
    """

    try:
        # AI генерира съдържанието, базирано на актуални данни
        response = model.generate_content(prompt)
        text = response.text
        
        # Почистване на JSON отговора
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        
        data = json.loads(text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Успешно анализирани {len(data)} топ мача!")

    except Exception as e:
        print(f"❌ Грешка: {e}")

if __name__ == "__main__":
    run()
