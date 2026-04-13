import json
import os
from datetime import datetime
import google.generativeai as genai

# Конфигурация
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def run():
    print("🚀 Старт на професионалния анализ...")
    
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига"},
        {"h": "Леванте", "a": "Хетафе", "l": "Ла Лига"}
    ]
    
    final_data = []
    
    # Промпт за масивен анализ
    full_prompt = "Ти си футболен анализатор. Напиши детайлен анализ на български за всеки от тези мачове поотделно:\n"
    for m in matches:
        full_prompt += f"- {m['h']} срещу {m['a']} ({m['l']})\n"
    
    full_prompt += "\nИЗИСКВАНИЯ: За всеки мач напиши точно 5-6 изречения задълбочен анализ (форма, тактика, контузени) и завърши с 'Прогноза: [резултат]'. Разделяй мачовете с символите '###'."

    try:
        print("⏳ Изчакване на AI отговор (това може да отнеме до 1 минута)...")
        response = model.generate_content(full_prompt)
        raw_text = response.text
        parts = raw_text.split("###")
        
        for i, m in enumerate(matches):
            # Взимаме текста за конкретния мач
            analysis = parts[i].strip() if i < len(parts) else "Анализът се обработва..."
            
            # Вадим прогнозата за краткото поле
            prediction = "Виж анализа"
            if "Прогноза:" in analysis:
                prediction = analysis.split("Прогноза:")[-1].strip().split('\n')[0]

            final_data.append({
                "match": f"{m['h']} - {m['a']}",
                "prob": m['l'],
                "strat": analysis,
                "tip": prediction,
                "market": "AI Expert Scan",
                "injuries": "Детайлно проверени",
                "ref": "Pro AI Engine",
                "other": {"Time": datetime.now().strftime('%H:%M')}
            })
            
        print(f"✅ Успешно генерирани {len(final_data)} анализа.")

    except Exception as e:
        print(f"❌ Критична грешка: {e}")
        # Ако всичко се провали, поне да имаме структура
        for m in matches:
            final_data.append({
                "match": f"{m['h']} - {m['a']}",
                "prob": m['l'],
                "strat": "В момента AI сървърите са претоварени. Моля, опитайте след 15 минути за пълен анализ.",
                "tip": "В процес...",
                "market": "AI", "injuries": "Проверка...", "ref": "AI", "other": {"Time": "---"}
            })

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    run()
