import json
import os
import requests
from datetime import datetime
import google.generativeai as genai

# Конфигурация на ключовете
FOOTBALL_API_KEY = "3c34769062325c77742b58535184b260"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_today_matches():
    """Извлича топ мачовете за деня от API-Football"""
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': FOOTBALL_API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    # Параметри за днешните мачове (статус NS = Not Started)
    params = {'date': datetime.now().strftime('%Y-%m-%d'), 'status': 'NS'}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        fixtures = data.get('response', [])
        # Филтрираме само по-значими лиги за по-качествен анализ
        top_leagues = [39, 140, 135, 78, 61, 172] # Англия, Испания, Италия, Германия, Франция, България
        filtered = [f for f in fixtures if f['league']['id'] in top_leagues]
        return filtered[:10] # Взимаме до 10 мача
    except Exception as e:
        print(f"Грешка при API: {e}")
        return []

def run():
    print("🌐 Стартиране на автоматичен скенер...")
    matches = get_today_matches()
    
    if not matches:
        print("⚠️ Няма намерени нови мачове за анализ.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')
    results = []

    for f in matches:
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        league = f['league']['name']
        match_id = f['fixture']['id']
        
        print(f"🧠 Анализиране на {home} vs {away}...")
        
        prompt = f"""
        Направи експертен футболен анализ за мача: {home} - {away} ({league}).
        Използвай своите възможности за търсене, за да намериш актуална информация за:
        1. ПОДРОБЕН АНАЛИЗ: Форма на отборите, тактически стил и последни резултати (минимум 150 думи).
        2. СЪСТАВИ: Кои ключови играчи отсъстват и как това променя баланса?
        3. СЪДИЯ: Кой е реферът и каква е неговата репутация за картони?
        4. ПРОГНОЗА: Дай конкретен съвет (пазар) и се обоснови подробно ЗАЩО.

        Върни резултата СТРОГО в JSON формат:
        {{
            "match": "{home} - {away}",
            "prob": "{league}",
            "strat": "Твоят подробен анализ тук...",
            "tip": "Твоята прогноза тук...",
            "market": "Коефициент (приблизителен)",
            "injuries": "Данни за съставите...",
            "ref": "Данни за съдията..."
        }}
        """

        try:
            response = model.generate_content(prompt)
            clean_json = response.text.replace('```json', '').replace('```', '').strip()
            analysis = json.loads(clean_json)
            results.append(analysis)
        except Exception as e:
            print(f"Грешка при анализ на мач {match_id}: {e}")

    # Записване на резултатите
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"✅ Успешно генерирани {len(results)} подробни анализа.")

if __name__ == "__main__":
    run()
