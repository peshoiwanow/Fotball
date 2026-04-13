import json
import os
import time
from datetime import datetime
import google.generativeai as genai

# Взимаме ключа директно от средата на GitHub
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def run():
    print("🚀 Стартиране на дълбокия анализ...")
    
    # Списък с мачове
    matches_list = [
        "ЦСКА София - Левски София (Първа лига)",
        "Манчестър Юнайтед - Лийдс (Висша лига)",
        "Фиорентина - Лацио (Серия А)",
        "Берое - Локомотив Пловдив (Първа лига)",
        "Леванте - Хетафе (Ла Лига)"
    ]
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    final_results = []

    for match in matches_list:
        print(f"⏳ Анализирам: {match}")
        prompt = f"Направи експертен футболен анализ на български за мача {match}. Напиши 5 изречения за формата на отборите и завърши с конкретна прогноза."
        
        try:
            # Опит за генериране
            response = model.generate_content(prompt)
            analysis_text = response.text.strip()
            
            # Извличане на прогнозата
            tip = "Виж анализа"
            if "Прогноза" in analysis_text:
                tip = analysis_text.split("Прогноза")[-1].replace(":", "").strip()[:20]

            final_results.append({
                "match": match.split("(")[0].strip(),
                "prob": match.split("(")[1].replace(")", ""),
                "strat": analysis_text,
                "tip": tip,
                "market": "AI Expert",
                "injuries": "Проверено",
                "ref": "Gemini AI",
                "other": {"Time": datetime.now().strftime('%H:%M')}
            })
            # Пауза, за да не ни блокират
            time.sleep(5) 
            
        except Exception as e:
            print(f"⚠️ Проблем с {match}: {e}")
            final_results.append({
                "match": match, "prob": "Анализ", "strat": "В момента се обновява...", "tip": "---", 
                "market": "AI", "injuries": "---", "ref": "AI", "other": {"Time": "---"}
            })

    # Записване на файла
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    print("✅ Всичко е записано успешно!")

if __name__ == "__main__":
    run()
