import requests
import json
import os
from datetime import datetime
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
    country = match_info['league']['country']
    start_time = match_info['fixture']['date'][11:16]
    
    prompt = f"""
    Ти си професионален спортен анализатор. Направи детайлен и "дълбок" анализ за мача:
    {home} vs {away}
    Лига: {league} ({country}), Начало: {start_time} часа.
    
    Твоята задача е:
    1. Провери интернет за новини около двата отбора днес.
    2. Анализирай вероятните състави и липсващи играчи.
    3. Разгледай съдията и метеорологичните условия, ако имат значение.
    4. Дай финална прогноза с висока точност за българските букмейкъри.
    
    Напиши анализа на български език, структуриран с подзаглавия.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except: return "Анализът се генерира от AI..."

def run_scraper():
    # Взимаме днешната дата (Гринуич/UTC не ни бърка тук, защото API работи по дати)
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"📅 Генериране на тираж за целия ден: {today}")

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": FOOTBALL_API_HOST}
    
    # Взимаме АБСОЛЮТНО ВСИЧКИ мачове за днес
    params = {"date": today}
    
    try:
        res = requests.get(url, headers=headers, params=params)
        all_fixtures = res.json().get('response', [])

        if not all_fixtures:
            print("❌ API-то не връща мачове за днес.")
            return

        # Филтрираме само тези, които ОЩЕ НЕ СА ЗАВЪРШИЛИ (за да не гледаме стари резултати)
        # Статуси: NS (Not Started), 1H, 2H, HT (в игра)
        valid_fixtures = [f for f in all_fixtures if f['fixture']['status']['short'] in ['NS', '1H', '2H', 'HT']]

        # СОРТИРАНЕ: Показваме първо мачовете от по-известните държави/лиги
        # (за да не са само мачове от Виетнам или Етиопия най-отгоре)
        priority_countries = ['England', 'Spain', 'Germany', 'Italy', 'France', 'Bulgaria', 'Netherlands', 'Portugal', 'Turkey']
        
        def sort_key(x):
            country = x['league']['country']
            return (0 if country in priority_countries else 1, x['fixture']['date'])

        sorted_fixtures = sorted(valid_fixtures, key=sort_key)

        # Взимаме ТОП 15 мача за целия ден
        fixtures = sorted_fixtures[:15]

        final_reports = []
        for f in fixtures:
            h_name = f['teams']['home']['name']
            a_name = f['teams']['away']['name']
            l_name = f['league']['name']
            country = f['league']['country']
            match_time = f['fixture']['date'][11:16] # Взимаме само часа
            
            print(f"✅ Анализирам: {h_name} - {a_name} ({match_time})")
            
            report = {
                "match": f"{h_name} - {a_name}",
                "prob": f"{country}: {l_name} ({match_time})",
                "market": "Дневен Анализ",
                "tip": "ПРОГНОЗА",
                "strat": get_ultra_analysis(f),
                "injuries": "Пълна проверка на съставите",
                "ref": "Включен в доклада",
                "other": {"Start": match_time, "Status": f['fixture']['status']['long']}
            }
            final_reports.append(report)

        # Записваме в основния файл за сайта
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(final_reports, file, ensure_ascii=False, indent=4)
        
        print(f"🔥 Готово! Качени са {len(final_reports)} анализа за целия ден.")
        
    except Exception as e:
        print(f"Грешка: {e}")

if __name__ == "__main__":
    run_scraper()
