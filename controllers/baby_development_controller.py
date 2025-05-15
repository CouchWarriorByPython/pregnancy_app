import json
import os

class BabyDevelopmentController:
    def __init__(self, data_file='resources/data/baby_development.json'):
        self.data_file = data_file
        self.development_data = self._load_development_data()
        
    def _load_development_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
        except Exception as e:
            print(f"Помилка при завантаженні даних про розвиток дитини: {e}")
        
        return {"weeks": {}}
    
    def get_week_data(self, week):
        week_str = str(week)
        if week_str in self.development_data.get("weeks", {}):
            return self.development_data["weeks"][week_str]
        return None
    
    def get_fruit_comparison(self, week):
        week_data = self.get_week_data(week)
        if week_data and "size" in week_data:
            return week_data["size"]
        return None

    def get_baby_development_info(self, week, gender=None):
        """Отримує інформацію про розвиток дитини з урахуванням статі"""
        week_data = self.get_week_data(week)
        if week_data:
            # Якщо стать відома, можемо показувати спеціальну інформацію
            if gender in ["Хлопчик", "Дівчинка"]:
                gender_key = "boy" if gender == "Хлопчик" else "girl"
                gender_info = week_data.get(f"{gender_key}_development", "")
                if gender_info:
                    return gender_info

            # За замовчуванням показуємо загальну інформацію
            return week_data.get("baby_development", "Інформація відсутня")
        return "Інформація відсутня"
    
    def get_mother_changes_info(self, week):
        week_data = self.get_week_data(week)
        if week_data:
            return week_data.get("mother_changes", "Інформація відсутня")
        return "Інформація відсутня"
    
    def get_nutrition_tips(self, week):
        week_data = self.get_week_data(week)
        if week_data:
            return week_data.get("nutrition_tips", "Інформація відсутня")
        return "Інформація відсутня"
    
    def get_baby_size(self, week):
        week_data = self.get_week_data(week)
        if week_data:
            return {
                "weight": week_data.get("weight", "невідомо"),
                "length": week_data.get("length", "невідомо")
            }
        return {"weight": "невідомо", "length": "невідомо"}
    
    def get_available_weeks(self):
        return sorted([int(week) for week in self.development_data.get("weeks", {}).keys()]) 