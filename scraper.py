import json
import os
import requests
import google.generativeai as genai
from datetime import datetime

# Ключове
FOOTBALL_API_KEY = "3c34769062325c77742b58535184b260"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА СКРАПЕРА...")
    genai.configure(api_key=GEMINI_API_KEY)
    
    # 1. Вземане на мачове - премахваме филтъра за лиги, за да сме сигурни, че ще намери нещо
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-rapidapi-key': FOOTBALL_API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    
    # Търсим мачове за днес
    today = datetime.now().strftime('%Y-%m-%d')
    params = {'date': today, 'status': 'NS'} # NS = Not Started (предстоящи)
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        res_data = response.json()
        fixtures = res_data.get('response', [])
        
        # Ако няма предстоящи за днес, търсим за утре
        if not fixtures:
            print("📅 Няма предстоящи мачове за днес, търся за утре...")
            from datetime import timedelta
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            params['date'] = tomorrow
            response = requests.get(url, headers=headers, params=params, timeout=15)
            fixtures = response.json().get('response', [])

        print(f"✅ Намерени {len(fixtures)} мача.")
        # Взимаме първите 5 мача, които намерим
        fixtures = fixtures[:5] 
        
    except Exception as e:
        print(f"❌ Грешка при API: {e}")
        return

    if not fixtures:
        print("❌ Не бяха намерени никакви мачове в API-то.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')
    final_data = []

    for f in fixtures:
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        league = f['league']['name']
        
        print(f"🔍 Анализирам: {home} - {away}")
        
        prompt = f"""Направи кратък, но професионален анализ за {home} - {away} ({league}). 
        Дай прогноза, контузии и информация за съдията. 
        Върни САМО чист JSON: {{"match": "{home} - {away}", "prob": "{league}", "strat": "...", "tip": "...", "market": "...", "injuries": "...", "ref": "..."}}"""

        try:
            res = model.generate_content(prompt)
            text = res.text.replace('```json', '').replace('```', '').strip()
            item = json.loads(text)
            final_data.append(item)
        except:
            continue

    # Записване на данните
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"🏁 УСПЕШНО: Записани {len(final_data)} мача.")

if __name__ == "__main__":
    run()
