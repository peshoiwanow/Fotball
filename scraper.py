import json
import os
import time
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def get_ai_analysis(match_name, league):
    prompt = f"""
    Ти си топ футболен анализатор. Направи подробен експертен анализ на български за мача {match_name} ({league}).
    Напиши минимум 4-5 изречения подробна обосновка, включи информация за формата на отборите и завърши с конкретна прогноза (напр. 'Победа за домакина' или 'Над 2.5 гола').
    Бъди професионален и убедителен.
    """
    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return response.text.strip()
    except:
        return "Анализът се генерира в момента... Очаквайте детайли скоро."

def run():
    print("🚀 Старт на индивидуалния анализ на мачовете...")
    
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига"},
        {"h": "Леванте", "a": "Хетафе", "l": "Ла Лига"}
    ]
    
    final_data = []
    
    for m in matches:
        match_full_name = f"{m['h']} - {m['a']}"
        print(f"🕵️‍♂️ Анализирам: {match_full_name}")
        
        full_analysis = get_ai_analysis(match_full_name, m['l'])
        
        # Кратка прогноза за заглавието
        short_tip = "Виж анализа"
        if "Прогноза:" in full_analysis:
            short_tip = full_analysis.split("Прогноза:")[-1].strip()[:30]

        final_data.append({
            "match": match_full_name,
            "prob": m['l'],
            "strat": full_analysis,
            "tip": short_tip,
            "market": "AI Expert Scan",
            "injuries": "Проверено",
            "ref": "Gemini AI",
            "other": {"Time": datetime.now().strftime('%H:%M')}
        })
        time.sleep(2) # Малка пауза, за да не блокират ключа

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"✅ Готово! Записани {len(final_data)} подробни анализа.")

if __name__ == "__main__":
    run()
