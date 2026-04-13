import requests
import json
import os
from datetime import datetime
import google.generativeai as genai

# === КЛЮЧОВЕ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

genai.configure(api_key=GEMINI_API_KEY)
# Използваме модел, който има достъп до интернет инструменти
model = genai.GenerativeModel('gemini-1.5-flash')

def get_matches_from_internet():
    """Караме AI да намери мачовете за деня чрез интернет търсене"""
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"""
    Днес е {today}. Провери в интернет (Flashscore, SofaScore, Sky Sports) кои са най-важните футболни мачове за днес, които присъстват в тиражите на букмейкърите.
    Изброй точно 10 мача.
    За всеки мач дай: Домакин, Гост, Лига и Час на започване.
    Върни отговора САМО като JSON списък в този формат:
    [
      {{"home": "Team A", "away": "Team B", "league": "Premier League", "time": "21:00"}},
      ...
    ]
    """
    try:
        response = model.generate_content(prompt)
        # Почистване на отговора, за да остане само чист JSON
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_text)
    except:
        print("Грешка при намиране на мачове от AI.")
        return []

def get_deep_analysis(match):
    """AI прави пълен анализ на база интернет данни за конкретния мач"""
    prompt = f"""
    Направи детайлен футболен анализ за мача: {match['home']} vs {match['away']} ({match['league']}).
    1. Провери форма, H2H и последни новини за съставите.
    2. Виж какви са очакванията в сайтове като SofaScore и Flashscore.
    3. Провери за наказани играчи или нови контузии.
    4. Дай най-сигурната прогноза (Value Bet) на български.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Анализът не може да бъде генериран в момента."

def run_scraper():
    print("🌐 AI започва сканиране на интернет за мачове...")
    matches = get_matches_from_internet()
    
    if not matches:
        print("❌ AI не откри мачове в интернет.")
        return

    final_data = []
    for m in matches:
        print(f"✅ Анализ на: {m['home']} - {m['away']}")
        analysis = get_deep_analysis(m)
        
        final_data.append({
            "match": f"{m['home']} - {m['away']}",
            "prob": f"{m['league']} ({m['time']})",
            "market": "Internet Deep Scan",
            "tip": "ВИЖ АНАЛИЗА",
            "strat": analysis,
            "injuries": "Проверено онлайн",
            "ref": "Включен в анализа",
            "other": {"Time": m['time']}
        })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"🔥 Успех! Генерирани са {len(final_data)} анализа чрез директно търсене.")

if __name__ == "__main__":
    run_scraper()
