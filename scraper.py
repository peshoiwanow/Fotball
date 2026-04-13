import json
import os
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Старт на анализа с новата библиотека Google GenAI...")
    
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига (България)"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига (Англия)"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига (България)"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А (Италия)"}
    ]

    final_data = []

    for m in matches:
        print(f"🕵️‍♂️ Анализ: {m['h']} - {m['a']}")
        prompt = f"Направи кратък анализ и прогноза на български за мача {m['h']} vs {m['a']} ({m['l']}) за днес, 13 април 2026."
        
        try:
            # Използваме новия метод за генериране
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            final_data.append({
                "match": f"{m['h']} - {m['a']}",
                "prob": m['l'],
                "strat": response.text,
                "tip": "ВИЖ ПРОГНОЗАТА",
                "market": "AI GenAI Scan",
                "injuries": "Проверено в реално време",
                "ref": "Виж анализа",
                "other": {"Updated": datetime.now().strftime('%H:%M')}
            })
        except Exception as e:
            print(f"❌ Грешка при {m['h']}: {e}")

    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! Записани са {len(final_data)} анализа.")
    else:
        print("⚠ Няма генерирани данни.")

if __name__ == "__main__":
    run()
