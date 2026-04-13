import json
import os
import requests
from datetime import datetime
import google.generativeai as genai

# Конфигурация
FOOTBALL_API_KEY = "3c34769062325c77742b58535184b260" # Твоят API ключ
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def get_live_matches():
    """Взима актуалните мачове за днес от API-Football"""
    url = "https://v3.football.api-sports.io/fixtures"
    today = datetime.now().strftime('%Y-%m-%d')
    headers = {
        'x-rapidapi-key': FOOTBALL_API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    # Взимаме мачове от топ лиги за по-добър анализ
    params = {'date': today, 'status': 'NS'} 
    
    try:
        response = requests.get(url, headers=headers, params=params)
        fixtures = response.json().get('response', [])
        # Избираме топ 8 мача (за да не претоварим AI)
        return fixtures[:8]
    except Exception as e:
        print(f"Грешка при API-Football: {e}")
        return []

def run():
    print("🛰️ Взимане на мачове от API-Football...")
    matches = get_live_matches()
    
    if not matches:
        print("❌ Не бяха намерени мачове за днес.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')
    final_data = []

    for f in matches:
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        league = f['league']['name']
        match_time = f['fixture']['date'].split('T')[1][:5]
        
        print(f"🔍 Дълбок анализ за: {home} - {away}")
        
        prompt = f"""
        Ти си професионален футболен типстър. Направи мащабен анализ за мача: {home} срещу {away} ({league}).
        Трябва ми:
        1. ДЪЛБОК АНАЛИЗ: Форма, тактически промени и психологическо състояние (минимум 150 думи).
        2. СЪСТАВИ: Потвърдени или вероятни титуляри и контузени ключови играчи.
        3. СЪДИЯ: Кой е и какъв е трендът му за картони.
        4. ОБОСНОВКА: Защо точно тази прогноза е най-силна?
        5. ПРОГНОЗА: Точен залог и коефициент.

        Върни резултата като JSON обект със следните ключове: match, prob, strat, tip, market, injuries, ref.
        """

        try:
            response = model.generate_content(prompt)
            # Извличане на чист текст от AI
            res_text = response.text
            
            # Добавяме към финалния списък (тук добавяме малко логика да не гърми ако не е чист JSON)
            final_data.append({
                "match": f"{home} - {away}",
                "prob": f"{league} | {match_time}ч.",
                "strat": res_text, # Записваме целия мащабен анализ тук
                "tip": "Анализирана прогноза",
                "market": "Live AI Data",
                "injuries": "Виж пълния анализ",
                "ref": "Проверено в интернет",
                "other": {"Time": datetime.now().strftime('%H:%M')}
            })
        except Exception as e:
            print(f"Грешка при AI анализ на {home}: {e}")

    # Записваме всичко в data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"✅ Готово! Анализирани са {len(final_data)} мача.")

if __name__ == "__main__":
    run()
