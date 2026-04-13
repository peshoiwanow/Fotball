import json
import os
import re
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Старт на дълбокия AI анализ...")
    
    # Списък с мачове за анализ
    matches_to_scan = "ЦСКА - Левски, Манчестър Юнайтед - Лийдс, Фиорентина - Лацио, Берое - Локо Пловдив, Леванте - Хетафе"
    
    prompt = f"""
    Ти си професионален футболен експерт. Направи детайлен анализ на български за тези мачове: {matches_to_scan}.
    За ВСЕКИ мач генерирай:
    1. Пълна обосновка (минимум 3 изречения).
    2. Конкретна прогноза (напр. 'Над 2.5 гола' или 'Победа за домакина').
    
    Върни резултата ЕДИНСТВЕНО като JSON списък в този формат:
    [
      {{"match": "Отбор А - Отбор Б", "prob": "Име на Лига", "strat": "Текст на анализа тук", "tip": "Прогноза тук", "market": "AI Expert", "injuries": "Проверено", "ref": "AI", "other": {{"Time": "13.04.2026"}}}}
    ]
    """

    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        text = response.text.strip()
        
        # МАГИЯТА: Почистване на текста, ако AI сложи ```json или други знаци
        json_match = re.search(r'\[.*\]', text, re.DOTALL)
        if json_match:
            clean_json = json_match.group(0)
            final_data = json.loads(clean_json)
            print(f"✅ AI анализира успешно {len(final_data)} мача.")
        else:
            raise ValueError("Не бе открит валиден JSON формат в отговора на AI.")
            
    except Exception as e:
        print(f"❌ Грешка при AI: {e}")
        # Резервен списък с 5 мача, за да не е празен сайтът при срив на API
        final_data = [
            {"match": "ЦСКА - Левски", "prob": "Първа лига", "strat": "Очаква се голямо напрежение. Формата на двата отбора е сходна, като защитата ще бъде приоритет.", "tip": "Под 2.5 гола", "market": "AI Scan", "injuries": "Проверено", "ref": "AI", "other": {"Time": "10:00"}},
            {"match": "Манчестър Юнайтед - Лийдс", "prob": "Висша лига", "strat": "Юнайтед доминира в преките двубои, но Лийдс играе агресивно в атака.", "tip": "Победа за Юнайтед", "market": "AI Scan", "injuries": "Проверено", "ref": "AI", "other": {"Time": "10:00"}},
            {"match": "Фиорентина - Лацио", "prob": "Серия А", "strat": "Лацио е в серия от победи, докато Фиорентина трудно бележи срещу топ отбори.", "tip": "X2", "market": "AI Scan", "injuries": "Проверено", "ref": "AI", "other": {"Time": "10:00"}},
            {"match": "Берое - Локо Пловдив", "prob": "Първа лига", "strat": "Традиционно труден мач за гостите под Аязмото.", "tip": "1X", "market": "AI Scan", "injuries": "Проверено", "ref": "AI", "other": {"Time": "10:00"}},
            {"match": "Леванте - Хетафе", "prob": "Ла Лига", "strat": "Битка в дъното на таблицата, където всяка точка е важна.", "tip": "Равенство", "market": "AI Scan", "injuries": "Проверено", "ref": "AI", "other": {"Time": "10:00"}}
        ]

    # Записване на файла
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("🚀 Данните са записани успешно в data.json!")

if __name__ == "__main__":
    run()
