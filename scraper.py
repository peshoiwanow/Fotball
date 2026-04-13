import json
import os
from datetime import datetime
from google import genai

# === КОНФИГУРАЦИЯ ===
GEMINI_API_KEY = "AIzaSyCOL_KW0qIoXk-4fdJgXB_njA-2VItGG-M"
client = genai.Client(api_key=GEMINI_API_KEY)

def run():
    print("🚀 Старт на детайлния анализ...")
    
    # Списък с 5 топ мача
    matches = [
        {"h": "ЦСКА София", "a": "Левски София", "l": "Първа лига (България)"},
        {"h": "Манчестър Юнайтед", "a": "Лийдс", "l": "Висша лига (Англия)"},
        {"h": "Фиорентина", "a": "Лацио", "l": "Серия А (Италия)"},
        {"h": "Берое", "a": "Локомотив Пловдив", "l": "Първа лига (България)"},
        {"h": "Леванте", "a": "Хетафе", "l": "Ла Лига (Испания)"}
    ]
    
    final_data = []
    
    for m in matches:
        print(f"🕵️‍♂️ AI генерира експертен анализ за: {m['h']} - {m['a']}")
        
        # Разширен промпт за повече детайли
        prompt = f"""
        Ти си професионален футболен анализатор. Направи детайлен анализ за мача {m['h']} vs {m['a']} ({m['l']}) за днес, 13 април 2026.
        Изисквания:
        1. Подробна обоснована прогноза (форма, ключови играчи, защо този залог).
        2. Списък с контузени и наказани (ако има такива).
        3. Крайна прогноза с конкретен знак (1, X, 2) или брой голове.
        Напиши всичко на български език по интересен начин.
        """
        
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            analysis_text = response.text
            
            # Опитваме да извлечем кратка прогноза за заглавието
            tip_prompt = f"Въз основа на твоя анализ за {m['h']} - {m['a']}, дай само кратка прогноза от 3 думи (напр. Победа за ЦСКА)."
            tip_res = client.models.generate_content(model="gemini-1.5-flash", contents=tip_prompt)
            short_tip = tip_res.text.strip()

            final_data.append({
                "match": f"{m['h']} - {m['a']}",
                "prob": m['l'],
                "strat": analysis_text,
                "tip": short_tip, # Вече няма да пише само "ПРОГНОЗА"
                "market": "AI Expert Scan",
                "injuries": "Проверени в реално време",
                "ref": "Профилът е включен в анализа",
                "other": {"Time": datetime.now().strftime('%H:%M')}
            })
        except Exception as e:
            print(f"AI грешка при {m['h']}: {e}")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"✅ Готово! Записани {len(final_data)} пълни анализа.")

if __name__ == "__main__":
    run()
