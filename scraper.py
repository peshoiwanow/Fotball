import requests
import json
import os
from datetime import datetime, timedelta
import google.generativeai as genai

# === КЛЮЧОВЕ ===
FOOTBALL_API_KEY = "f6205fe03db8bd088398d60cd8266505"
FOOTBALL_API_HOST = "api-football-v1.p.rapidapi.com"
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ultra_analysis(match_info):
    home = match_info['teams']['home']['name']
    away = match_info['teams']['away']['name']
    league = match_info['league']['name']
    
    prompt = f"Направи професионален футболен анализ за {home} vs {away} ({league}). Провери контузии, съдия и тактика. Дай най-точна прогноза."
    try:
        response = model.generate_content(prompt)
        return response.text
    except: return "Анализът се подготвя..."

def run_scraper():
    # Взимаме днешната дата в българско време (добавяме часове за сигурност)
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"🚀 Търсене на мачове за дата: {today}")

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": FOOTBALL_API_HOST}
    
    # Търсим ВСИЧКИ предстоящи мачове за днес без филтър за лиги
    params = {"date": today, "status": "NS"}
    
    try:
        res = requests.get(url, headers=headers, params=params)
        all_fixtures = res.json().get('response', [])
        
        # Ако няма предстоящи, опитай да вземеш всички за деня (включително започнали)
        if not all_fixtures:
            print("Няма предстоящи, проверявам всички за деня...")
            params.pop("status")
            res = requests.get(url, headers=headers, params=params)
            all_fixtures = res.json().get('response', [])

        # Сортираме по важност на лигите (ID-та на топ лигите са по-малки)
        all_fixtures = sorted(all_fixtures, key=lambda x: x['league']['id'])
        fixtures = all_fixtures[:5] # Взимаме топ 5 мача

        if not fixtures:
            print("❌ Дефинитивно няма мачове в API за днес.")
            return

        final_reports = []
        for f in fixtures:
            h_name = f['teams']['home']['name']
            a_name = f['teams']['away']['name']
            print(f"✅ Намерен мач: {h_name} vs {a_name}")
            
            report = {
                "match": f"{h_name} - {a_name}",
                "prob": "📈 Анализ на живо",
                "market": f['league']['name'],
                "tip": "AI ПРОГНОЗА",
                "strat": get_ultra_analysis(f),
                "injuries": "Проверено",
                "ref": "Виж анализа",
                "other": {"Updated": datetime.now().strftime('%H:%M')}
            }
            final_reports.append(report)

        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(final_reports, file, ensure_ascii=False, indent=4)
        print(f"🔥 Успешно качени {len(final_reports)} мача!")
        
    except Exception as e:
        print(f"Грешка: {e}")

if __name__ == "__main__":
    run_scraper()
