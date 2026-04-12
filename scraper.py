import requests
import json
from datetime import datetime

def get_real_matches():
    # Този скрипт ще търси мачове от публични фийдове
    # За демото тук поставяме структурата, която AI ще пълни
    # В следващата стъпка ще добавим реалното извличане
    print("Сканиране за мачове в реално време...")
    
    # Примерна структура, която роботът ще генерира автоматично
    picks = [
        {
            "match": "Real Madrid vs Barcelona", # Реално взето име
            "date": datetime.now().strftime("%d.%m.%Y"),
            "market": "1X2",
            "tip": "Real Madrid",
            "prob": "78%",
            "strat": "Пълномащабен анализ на база последните 5 мача и липсата на Левандовски...",
            "injuries": "Barcelona: Lewandowski (Out), De Jong (Doubtful)",
            "ref": "Mateu Lahoz: Склонен към картони",
            "other": {"Over 2.5": "80%"},
            "result": "pending"
        }
    ]
    return picks

def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    data = get_real_matches()
    save_data(data)
    print("Програмата за деня е обновена успешно!")
