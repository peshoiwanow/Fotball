import json
import os
from datetime import datetime
from google import genai

# === КЛЮЧ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Старт на машината...")
    
    matches_list = "ЦСКА - Левски, Манчестър Юнайтед - Лийдс, Фиорентина - Лацио, Берое - Локо Пловдив, Леванте - Хетафе"
    
    prompt = f"""
    Направи футболни анализи за тези мачове: {matches_list}.
    Върни резултата САМО като чист JSON списък. Без обяснения отвън.
    Формат:
    [
      {{"match": "Отбор А - Отбор Б", "prob": "Лига", "strat": "Подробен анализ на български", "tip": "Прогноза", "market": "AI Expert", "injuries": "Проверено", "ref": "AI", "other": {{"Time": "13.04.2026"}}}}
    ]
    """

    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        raw_text = response.text.strip()
        
        # Почистване на текста от евентуални знаци на AI
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
        final_data = json.loads(raw_text)
        print(f"✅ AI генерира успешно {len(final_data)} анализа.")
        
    except Exception as e:
        print(f"❌ Грешка: {e}. Използвам резервен план.")
        # Резервен вариант, за да имаш мачове на сайта при проблем с AI
        final_data = [{
            "match": "ЦСКА - Левски", "prob": "Първа лига", "strat": "Очаква се оспорван мач...", "tip": "1X", "market": "AI", "injuries": "Проверено", "ref": "AI", "other": {"Time": "10:00"}
        }]

    # Записване
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("🚀 Файлът data.json е обновен успешно!")

if __name__ == "__main__":
    run()
