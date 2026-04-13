import json
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Генериране на мачове...")
    
    # Списък с 5 мача за днес
    matches_list = "ЦСКА - Левски, Ман Юнайтед - Лийдс, Фиорентина - Лацио, Берое - Локо Пловдив, Леванте - Хетафе"
    
    prompt = f"""
    Направи детайлни футболни прогнози за следните мачове: {matches_list}.
    За всеки мач напиши:
    1. Анализ на формата и съставите на български.
    2. Конкретна прогноза (например: 'Победа за домакина' или 'Над 2.5 гола').
    Върни резултата САМО като JSON списък точно в този формат:
    [
      {{"match": "Отбор А - Отбор Б", "prob": "Лига", "strat": "Текст на анализа", "tip": "Прогноза", "market": "AI Expert", "injuries": "Проверено", "ref": "AI", "other": {{"Time": "13.04.2026"}}}}
    ]
    """

    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        text = response.text.strip()
        
        # Изчистване на JSON отговора
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        data = json.loads(text)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! Записани {len(data)} мача.")
        
    except Exception as e:
        print(f"❌ ГРЕШКА: {e}")

if __name__ == "__main__":
    run()
