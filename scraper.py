import json
import os
from datetime import datetime
import google.generativeai as genai

# === КОНФИГУРАЦИЯ ===
# Използваме директен ключ за достъп
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

genai.configure(api_key=GEMINI_API_KEY)

# Опитваме с алтернативно име на модела, което е по-стабилно за v1beta
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

def run_deep_ai_analysis():
    print(f"🌐 AI стартира проучване за {datetime.now().strftime('%d.%m.%Y')}...")
    
    search_prompt = """
    Днес е 13 април 2026 г. Изброй 5-те най-важни футболни мача за днес в Европа и България.
    Върни ги САМО като JSON списък: 
    [{"home": "Отбор1", "away": "Отбор2", "league": "Лига", "time": "Час"}]
    """
    
    try:
        # Генериране на съдържание
        response = model.generate_content(search_prompt)
        
        if not response.text:
            print("❌ AI върна празен отговор.")
            return

        json_str = response.text.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
            
        matches = json.loads(json_str)
        print(f"✅ Намерени {len(matches)} мача.")
        
        final_data = []
        for m in matches:
            print(f"🕵️‍♂️ Анализирам {m['home']} - {m['away']}...")
            analysis_prompt = f"Направи кратък футболен анализ и прогноза на български за {m['home']} vs {m['away']}."
            analysis_res = model.generate_content(analysis_prompt)
            
            final_data.append({
                "match": f"{m['home']} - {m['away']}",
                "prob": f"{m['league']} ({m['time']})",
                "market": "AI Analysis",
                "tip": "ПРОГНОЗА",
                "strat": analysis_res.text,
                "injuries": "Проверено",
                "ref": "Виж анализа",
                "other": {"Updated": datetime.now().strftime('%H:%M')}
            })

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print("🚀 Успешно обновяване на data.json!")

    except Exception as e:
        print(f"❌ КРИТИЧНА ГРЕШКА: {str(e)}")

if __name__ == "__main__":
    run_deep_ai_analysis()
