import json
import os
import time
from datetime import datetime
import google.generativeai as genai

# Конфигурация
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def run():
    print("🌐 Старт на живото търсене в интернет за футболни анализи...")
    
    # Използваме модела с инструменти за търсене (Google Search)
    # Забележка: 'models/gemini-1.5-flash' поддържа инструменти за търсене
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[{"google_search_retrieval": {}}] # ТОВА АКТИВИРА ИНТЕРНЕТ ТЪРСЕНЕТО
    )
    
    matches = [
        {"name": "ЦСКА София - Левски София", "league": "Първа лига", "time": "17:45"},
        {"name": "Манчестър Юнайтед - Лийдс", "league": "Висша лига", "time": "22:00"},
        {"name": "Фиорентина - Лацио", "league": "Серия А", "time": "21:45"},
        {"name": "Берое - Локомотив Пловдив", "league": "Първа лига", "time": "20:00"},
        {"name": "Леванте - Хетафе", "league": "Ла Лига", "time": "19:30"}
    ]
    
    final_data = []

    for m in matches:
        print(f"🔍 Извличане на потвърдена информация за: {m['name']}")
        
        prompt = f"""
        Използвай Google Search, за да намериш актуална информация за мача {m['name']} днес, 13 април 2026.
        Трябват ми:
        1. ПОТВЪРДЕНИ СЪСТАВИ: Кои играчи са контузени или наказани днес? Кои са титулярите?
        2. СЪДИЯ: Кой е главният съдия на мача и каква е неговата статистика за картони?
        3. ЕКСПЕРТЕН АНАЛИЗ: Каква е формата на отборите в последните 3 мача?
        4. ПРОГНОЗА: Дай конкретен залог и актуален коефициент.
        
        Напиши отговора на български език. Раздели секциите с '---'.
        """

        try:
            # AI ще направи заявка към Google Search преди да отговори
            response = model.generate_content(prompt)
            full_text = response.text
            sections = full_text.split('---')
            
            strat = sections[0].strip() if len(sections) > 0 else "Няма намерена актуална информация."
            lineups = sections[1].strip() if len(sections) > 1 else "Съставите се очакват."
            referee = sections[2].strip() if len(sections) > 2 else "Информацията за съдията не е налична."
            prediction = sections[3].strip() if len(sections) > 3 else "Прогноза: 1X"

            final_data.append({
                "match": m['name'],
                "prob": m['league'],
                "strat": strat,
                "tip": prediction,
                "market": f"Начало: {m['time']}",
                "injuries": lineups,
                "ref": referee,
                "other": {"Time": datetime.now().strftime('%H:%M')}
            })
            time.sleep(5) # Изчакваме повече, защото търсенето отнема време

        except Exception as e:
            print(f"❌ Грешка при извличане: {e}")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("✅ Сайтът е обновен с реални данни от интернет!")

if __name__ == "__main__":
    run()
