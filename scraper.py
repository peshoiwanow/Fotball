import json
import os
import time
from datetime import datetime
import google.generativeai as genai

# Конфигурация
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def run():
    print("🌐 СТАРТ: Дълбоко сканиране на интернет (Flashscore, Sofascore, Новини)...")
    
    # Използваме модела с активирано търсене в реално време
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{'google_search_retrieval': {}}] 
    )

    prompt = """
    Днес е 13 април 2026. Използвай Google Search и изпълни следните задачи:
    1. Намери 5-те най-важни футболни мача за днес от топ лигите и България.
    2. За всеки мач извлечи: 
       - ПОТВЪРДЕНИ СЪСТАВИ: Кои са титулярите и кои са контузени?
       - СЪДИЯ: Кой е той и какъв е трендът му за картони?
       - НОВИНИ: Има ли скандали, нов треньор или промяна в тактиката?
    3. Направи масивен анализ (минимум 150 думи) за всеки мач, който обяснява защо дадената прогноза е най-логична.
    
    Върни резултата САМО като чист JSON списък:
    [
      {
        "match": "Отбор А - Отбор Б",
        "prob": "Лига | Начален час",
        "strat": "ДЪЛБОК АНАЛИЗ: Тук напиши огромна обосновка с факти от интернет.",
        "tip": "Прогноза и Коефициент",
        "market": "Коефициент",
        "injuries": "ПОДРОБНИ СЪСТАВИ: Списък с играчи.",
        "ref": "СЪДИЯ: Име и статистика.",
        "other": {"Time": "13.04.2026"}
      }
    ]
    """

    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # Премахване на излишни символи, ако AI добави такива
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        
        final_data = json.loads(text.strip())
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Успех! Анализирани са {len(final_data)} мача с данни от мрежата.")

    except Exception as e:
        print(f"❌ Критична грешка при търсенето: {e}")

if __name__ == "__main__":
    run()
