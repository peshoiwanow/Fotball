import json
import os
import requests
import google.generativeai as genai
from datetime import datetime

# Настройка на ключовете
FOOTBALL_API_KEY = "3c34769062325c77742b58535184b260"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА СКРАПЕРА...")
    
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва GEMINI_API_KEY в GitHub Secrets!")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    # 1. Вземане на мачове от API
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {'x-rapidapi-key': FOOTBALL_API_KEY, 'x-rapidapi-host': 'v3.football.api-sports.io'}
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        fixtures = response.json().get('response', [])[:5] # Вземаме само 5 за сигурност
        print(f"✅ Намерени {len(fixtures)} мача за анализ.")
    except Exception as e:
        print(f"❌ Грешка при API-Football: {e}")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')
    final_data = []

    for f in fixtures:
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        league = f['league']['name']
        
        prompt = f"Направи кратък, но дълбок анализ за {home} - {away} ({league}). Дай прогноза, контузии и съдия. Върни САМО чист JSON в този формат: {{\"match\": \"...\", \"prob\": \"...\", \"strat\": \"...\", \"tip\": \"...\", \"market\": \"...\", \"injuries\": \"...\", \"ref\": \"...\"}}"

        try:
            res = model.generate_content(prompt)
            # Почистване на JSON отговора от AI "маркери"
            text = res.text.replace('```json', '').replace('```', '').strip()
            item = json.loads(text)
            final_data.append(item)
            print(f"✅ Анализиран: {home}")
        except Exception as e:
            print(f"⚠️ Пропуск на мач поради грешка в AI: {e}")

    # Записване на файла
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("🏁 СКРАПЕРЪТ ЗАВЪРШИ УСПЕШНО!")

if __name__ == "__main__":
    run()
