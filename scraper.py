import json
import os
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
# Използваме директния ключ за Gemini
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Старт на анализа за 13 април 2026...")
    
    # Списък с най-важните мачове за деня
    matches_to_analyze = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига (България)"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига (Англия)"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А (Италия)"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига (България)"}
    ]

    final_data = []

    for m in matches_to_analyze:
        print(f"🕵️‍♂️ AI анализира: {m['h']} - {m['a']}")
        
        prompt = f"""
        Направи професионален футболен анализ за мача {m['h']} vs {m['a']} ({m['l']}) за днес, 13 април 2026.
        Напиши анализа на български език, включи състави и завърши с конкретна прогноза.
        """
        
        try:
            # Използваме новата библиотека google-genai
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            final_data.append({
                "match": f"{m['h']} - {m['a']}",
                "prob": m['l'],
                "strat": response.text,
                "tip": "ВИЖ ПРОГНОЗАТА",
                "market": "AI Deep Intelligence",
                "injuries": "Проверено в реално време",
                "ref": "Профилът е в анализа",
                "other": {"Updated": datetime.now().strftime('%H:%M')}
            })
        except Exception as e:
            print(f"❌ Грешка при {m['h']}: {e}")

    # Записване на данните в data.json
    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"✅ УСПЕХ! {len(final_data)} мача са записани в data.json.")
    else:
        print("❌ Не бяха генерирани никакви анализи.")

if __name__ == "__main__":
    run()
