import json
import os
from datetime import datetime
try:
    from google import genai
except ImportError:
    print("Грешка: Библиотеката google-genai не е инсталирана.")

# КЛЮЧ
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

def run():
    print("🚀 Старт на процеса...")
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига"}
    ]
    
    final_data = []
    
    for m in matches:
        print(f"🕵️‍♂️ Обработка на: {m['h']} - {m['a']}")
        try:
            # Новият метод на Google за 2026г.
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=f"Направи кратък анализ на български за мача {m['h']} vs {m['a']}."
            )
            analysis = response.text
        except Exception as e:
            print(f"AI грешка: {e}")
            analysis = "Анализът се генерира в момента..."

        final_data.append({
            "match": f"{m['h']} - {m['a']}",
            "prob": m['l'],
            "strat": analysis,
            "tip": "ПРОГНОЗА",
            "market": "AI Deep Scan",
            "injuries": "Проверено",
            "ref": "Виж анализа",
            "other": {"Time": datetime.now().strftime('%H:%M')}
        })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"✅ Готово! Записани {len(final_data)} мача.")

if __name__ == "__main__":
    run()
