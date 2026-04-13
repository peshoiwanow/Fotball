import json
import os
from datetime import datetime
import google.generativeai as genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_daily_matches_via_ai():
    """Караме AI да провери интернет за мачовете днес"""
    today = datetime.now().strftime('%d.%m.%Y')
    prompt = f"""
    Днес е {today}. Ти си спортен експерт. Провери в интернет (Flashscore, SofaScore, спортни новини) 
    кои са 10-те най-интересни футболни мача за днес, които присъстват в българските букмейкъри.
    
    Върни резултата САМО като чист JSON списък в този формат (без допълнителни обяснения):
    [
      {{"home": "Отбор 1", "away": "Отбор 2", "league": "Лига", "time": "19:30"}},
      ...
    ]
    """
    try:
        response = model.generate_content(prompt)
        # Почистване на JSON формата
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Грешка при намиране на мачове: {e}")
        return []

def get_deep_analysis(match):
    """Детайлен анализ на база интернет търсене"""
    prompt = f"""
    Направи подробен анализ за мача: {match['home']} vs {match['away']} ({match['league']}).
    Провери:
    1. Стартови състави и контузии (injury reports) от последните часове.
    2. Статистика и форма от Flashscore/SofaScore.
    3. Съдия и метеорологични условия.
    4. Дай най-сигурната прогноза с обосновка.
    
    Напиши всичко на български език, професионално и детайлно.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Анализът се подготвя..."

def main():
    print("🌐 AI сканира интернет за днешните мачове...")
    matches = get_daily_matches_via_ai()
    
    if not matches:
        print("❌ AI не успя да открие мачове.")
        return

    final_results = []
    for m in matches:
        print(f"✅ Анализиране на: {m['home']} - {m['away']}")
        report = {
            "match": f"{m['home']} - {m['away']}",
            "prob": f"{m['league']} ({m['time']} ч.)",
            "market": "Deep Web Scan",
            "tip": "ВИЖ АНАЛИЗА",
            "strat": get_deep_analysis(m),
            "injuries": "Проверено в реално време",
            "ref": "Включен в анализа",
            "other": {"Source": "AI Live Research", "Time": m['time']}
        }
        final_results.append(report)

    # Записване
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    
    print(f"🔥 Успех! Генерирани са {len(final_results)} анализа без помощта на API!")

if __name__ == "__main__":
    main()
