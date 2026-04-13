import json
import os
import time
from datetime import datetime
import google.generativeai as genai

# Взимаме ключа директно
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def run():
    print("🚀 Старт на професионалния спортен анализ...")
    
    # Списък с мачове за днес
    matches = [
        {"name": "ЦСКА София - Левски София", "league": "Първа лига", "time": "17:45"},
        {"name": "Манчестър Юнайтед - Лийдс", "league": "Висша лига", "time": "22:00"},
        {"name": "Фиорентина - Лацио", "league": "Серия А", "time": "21:45"},
        {"name": "Берое - Локомотив Пловдив", "league": "Първа лига", "time": "20:00"},
        {"name": "Леванте - Хетафе", "league": "Ла Лига", "time": "19:30"}
    ]
    
    final_data = []

    for m in matches:
        print(f"📡 Анализиране на реални данни за: {m['name']}")
        
        prompt = f"""
        Направи експертен преглед за мача {m['name']} днес, 13 април 2026.
        Изисквам ПЪЛНА ИНФОРМАЦИЯ:
        1. ПОДРОБЕН АНАЛИЗ: Форма, тактика и очаквания (минимум 6 изречения).
        2. СЪСТАВИ И ТРАВМИ: Кои са контузените играчи и какъв е очакваният стартов състав?
        3. СЪДИЯ: Кой е съдията и какъв е неговият стил (картони)?
        4. ПРОГНОЗА: Дай конкретен залог и актуален коефициент.
        
        Напиши отговора на български език. Раздели секциите с '---'.
        """

        try:
            response = model.generate_content(prompt)
            full_text = response.text
            sections = full_text.split('---')
            
            # Попълване на данните
            strat = sections[0].strip() if len(sections) > 0 else "Анализът се подготвя..."
            lineups = sections[1].strip() if len(sections) > 1 else "Няма информация за липсващи играчи."
            referee = sections[2].strip() if len(sections) > 2 else "Информация за съдията: Предстои обявяване."
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
            time.sleep(3) # Пауза за стабилност

        except Exception as e:
            print(f"⚠️ Грешка при {m['name']}: {e}")

    # Записване
    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Успешно записани {len(final_data)} мача с пълни данни.")

if __name__ == "__main__":
    run()
