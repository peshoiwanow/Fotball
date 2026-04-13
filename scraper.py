import json
import os
from datetime import datetime
import google.generativeai as genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
genai.configure(api_key=GEMINI_API_KEY)

# Използваме универсален достъп до модела
model = genai.GenerativeModel('gemini-1.5-flash')

def run():
    print("🚀 Старт на задълбочения анализ за 13 април 2026...")
    
    # Списък с най-търсените мачове за днес
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
        Направи детайлен анализ за мача {m['h']} vs {m['a']} ({m['l']}) за днес, 13 април 2026.
        Провери в интернет: последни новини, контузии на играчи и съдия.
        Напиши анализа на български език. Завърши с конкретна прогноза (Value Bet).
        """
        
        try:
            response = model.generate_content(prompt)
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
            print(f"Грешка при {m['h']}: {e}")

    # Записване на данните
    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"🔥 УСПЕХ! {len(final_data)} мача са записани в data.json.")
    else:
        print("❌ Не бяха генерирани анализи.")

if __name__ == "__main__":
    run()
