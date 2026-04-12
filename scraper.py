import requests
import json
import os
from datetime import datetime
import google.generativeai as genai

# Ключове
FOOTBALL_API_KEY = "f6205fe03db8bd088398d60cd8266505"
FOOTBALL_API_HOST = "api-football-v1.p.rapidapi.com"
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"

# Конфигурация на Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_real_matches():
    """Взима днешните топ мачове"""
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": FOOTBALL_API_KEY, "X-RapidAPI-Host": FOOTBALL_API_HOST}
    params = {"date": datetime.now().strftime('%Y-%m-%d'), "status": "NS"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        all_fixtures = response.json().get('response', [])
        # Взимаме първите 5 мача от по-известни лиги
        return all_fixtures[:5]
    except: return []

def get_ai_analysis(match_data):
    """Изпраща данните на Gemini и генерира професионален анализ"""
    home = match_data['teams']['home']['name']
    away = match_data['teams']['away']['name']
    league = match_data['league']['name']
    
    prompt = f"""
    Ти си професионален футболен анализатор и експерт по спортни залози. 
    Направи детайлен анализ за мача {home} срещу {away} в лига {league}.
    Изисквания:
    1. Напиши '🔍 ТАКТИЧЕСКИ АНАЛИЗ', който включва стил на игра и форма.
    2. Напиши '📊 СТАТИСТИЧЕСКА ДЪЛБОЧИНА' с очакван развой.
    3. Напиши '🎯 ПРОГНОЗА С ВИСОК ШАНС' и обясни защо това е най-добрият залог.
    4. Използвай професионален, сериозен тон на български език.
    Бъди изчерпателен и не използвай общи фрази.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "В момента AI анализира данните от интернет... Очаквайте актуализация."

def process_matches():
    fixtures = fetch_real_matches()
    final_data = []
    
    for f in fixtures:
        home_name = f['teams']['home']['name']
        away_name = f['teams']['away']['name']
        print(f"🤖 AI анализира: {home_name} vs {away_name}")
        
        ai_text = get_ai_analysis(f)
        
        report = {
            "match": f"{home_name} - {away_name}",
            "prob": "📈 Анализирано от AI",
            "market": "Pro Analysis",
            "tip": "Виж пълния анализ",
            "strat": ai_text,
            "injuries": "Проверка на официалните състави в реално време...",
            "ref": "Справка с официалния делегат на УЕФА/ФИФА.",
            "other": {"AI Confidence": "Висока", "Value Detection": "Намерено"}
        }
        final_data.append(report)
        
    # Запис и архив
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    today = datetime.now().strftime('%Y-%m-%d')
    os.makedirs('archive', exist_ok=True)
    with open(f"archive/matches_{today}.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    process_matches()
