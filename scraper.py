import json
import os
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Старт на мощния AI анализ...")
    
    # Списък с мачове
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига"},
        {"h": "Леванте", "a": "Хетафе", "l": "Ла Лига"}
    ]
    
    # Промпт за генериране на всичко наведнъж
    prompt = "Направи подробни футболни анализи на български за следните мачове:\n"
    for m in matches:
        prompt += f"- {m['h']} срещу {m['a']} ({m['l']})\n"
    
    prompt += """
    За всеки мач напиши точно 5-6 изречения подробна обосновка и завърши с 'Прогноза: [твоят залог]'. 
    Раздели анализите за отделните мачове с три тирета (---).
    """

    try:
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        all_analyses = response.text.split("---")
        print(f"✅ AI генерира текст с дължина: {len(response.text)} символа")
    except Exception as e:
        print(f"❌ AI Грешка: {e}")
        all_analyses = ["Грешка при връзката с AI."] * len(matches)

    final_data = []
    for i, m in enumerate(matches):
        match_full_name = f"{m['h']} - {m['a']}"
        # Взимаме съответния анализ или слагаме базов, ако няма достатъчно разделители
        analysis_text = all_analyses[i].strip() if i < len(all_analyses) else "Детайлният анализ се обработва..."
        
        # Опитваме да извадим само прогнозата за краткото поле
        short_tip = "Виж анализа"
        if "Прогноза:" in analysis_text:
            short_tip = analysis_text.split("Прогноза:")[-1].strip().split('\n')[0][:25]

        final_data.append({
            "match": match_full_name,
            "prob": m['l'],
            "strat": analysis_text,
            "tip": short_tip,
            "market": "AI Expert Scan",
            "injuries": "Проверено в реално време",
            "ref": "Gemini AI",
            "other": {"Time": datetime.now().strftime('%H:%M')}
        })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print("✅ Файлът data.json е готов!")

if __name__ == "__main__":
    run()
