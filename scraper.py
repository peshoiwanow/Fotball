import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def run():
    print("🚀 СТАРТ НА ДИАГНОСТИКАТА...")
    if not GEMINI_API_KEY:
        print("❌ ГРЕШКА: Липсва API Ключ!")
        return

    # Стъпка 1: Проверка кои модели са достъпни за теб
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    try:
        models_resp = requests.get(list_url)
        models_data = models_resp.json()
        
        if 'error' in models_data:
            print(f"❌ API ГРЕШКА ПРИ СПИСЪК: {models_data['error']['message']}")
            return

        # Търсим модел, който поддържа генериране на съдържание
        available_models = [m['name'] for m in models_data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        
        if not available_models:
            print("❌ Google не ти позволява достъп до нито един модел в момента.")
            return

        # Избираме първия наличен модел (обикновено gemini-1.5-flash)
        selected_model = available_models[0]
        print(f"✅ Избран работещ модел: {selected_model}")

        # Стъпка 2: Изпълнение на анализа с намерения модел
        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={GEMINI_API_KEY}"
        
        prompt = "Намери 5 футболни мача за днес и върни JSON списък с ключове: match, tip, prob."
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }

        response = requests.post(gen_url, json=payload, timeout=60)
        res_data = response.json()

        if 'error' in res_data:
            print(f"❌ ГРЕШКА ПРИ ГЕНЕРИРАНЕ: {res_data['error']['message']}")
            return

        text = res_data['candidates'][0]['content']['parts'][0]['text']
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(json.loads(text), f, ensure_ascii=False, indent=4)
        print("✅ УСПЕХ! Данните са записани успешно.")

    except Exception as e:
        print(f"❌ Критична грешка: {str(e)}")

if __name__ == "__main__":
    run()
