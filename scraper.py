import json
import os
from datetime import datetime
import google.generativeai as genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def run():
    print("🚀 Старт на анализа за 13 април 2026...")
    
    # Списък с топ мачове за деня
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига (България)"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига (Англия)"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига (България)"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А (Италия)"}
    ]

    final_data = []

    for m in matches:
        print(f"🕵️‍♂️ Анализ: {m['h']} - {m['a']}")
        prompt = f"Направи кратък анализ и прогноза на български за {m['h']} vs {m['a']} ({m['l']}) за днес."
        
        try:
            response = model.generate_content(prompt)
            final_data.append({
                "match": f"{m['h']} - {m['a']}",
                "prob": m['l'],
                "strat": response.text,
                "tip": "ВИЖ ПРОГНОЗАТА",
                "market": "AI Scan",
                "injuries": "Проверено",
                "ref": "Виж анализа",
                "other": {"Updated": datetime.now().strftime('%H:%M')}
            })
        except Exception as e:
            print(f"Грешка: {e}")

    # Записване
    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Успешно записани {len(final_data)} мача!")

if __name__ == "__main__":
    run()
