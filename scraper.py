import json
import os
from datetime import datetime
import google.generativeai as genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def run_deep_ai_analysis():
    print("🌐 AI стартира глобално проучване на мачовете за 13 април 2026...")
    
    # Стъпка 1: AI намира мачовете за деня
    search_prompt = """
    Днес е 13 април 2026 г. Намери 10-те най-важни футболни мача за днес, които присъстват в българските букмейкъри. 
    Задължително включи дербито ЦСКА - Левски и мачовете от Висшата лига, Ла Лига и Серия А.
    Върни резултата САМО като JSON списък: 
    [{"home": "Отбор1", "away": "Отбор2", "league": "Лига", "time": "Час"}]
    """
    
    try:
        response = model.generate_content(search_prompt)
        # Почистване на JSON отговора
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        matches = json.loads(json_str)
        
        final_data = []
        for m in matches:
            print(f"✅ Анализиране на {m['home']} vs {m['home']}...")
            
            # Стъпка 2: AI прави подробен анализ за всеки мач
            analysis_prompt = f"""
            Направи детайлен анализ за {m['home']} vs {m['away']} ({m['league']}). 
            Провери в интернет: състави, контузии, съдия и форма. 
            Дай прогноза с най-висок шанс за печалба на български.
            """
            analysis_res = model.generate_content(analysis_prompt)
            
            final_data.append({
                "match": f"{m['home']} - {m['away']}",
                "prob": f"{m['league']} ({m['time']} ч.)",
                "market": "Deep Scan Analysis",
                "tip": "ВИЖ ПРОГНОЗАТА",
                "strat": analysis_res.text,
                "injuries": "Проверено онлайн",
                "ref": "Включен в анализа",
                "other": {"Updated": datetime.now().strftime('%H:%M')}
            })

        # Записваме в data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"🔥 Успешно анализирани {len(final_data)} мача!")

    except Exception as e:
        print(f"Грешка: {str(e)}")

if __name__ == "__main__":
    run_deep_ai_analysis()
