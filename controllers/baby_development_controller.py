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
                    return json.load(f)
        except Exception as e:
            print(f"Помилка при завантаженні даних про розвиток дитини: {e}")
        return {"weeks": {}}

    def get_week_data(self, week):
        return self.development_data.get("weeks", {}).get(str(week))

    def _get_week_info(self, week, field, default="Інформація відсутня"):
        week_data = self.get_week_data(week)
        return week_data.get(field, default) if week_data else default

    def get_fruit_comparison(self, week):
        week_data = self.get_week_data(week)
        if not week_data:
            return None

        fruit_data = {
            "fruit": week_data["size"]["fruit"],
            "description": week_data["size"]["description"]
        }

        if "image" in week_data:
            fruit_data["image"] = week_data["image"]
        else:
            default_image = f"resources/images/fruits/{week}.png"
            if os.path.exists(default_image):
                fruit_data["image"] = default_image

        return fruit_data

    def get_baby_development_info(self, week, gender=None):
        week_data = self.get_week_data(week)
        if not week_data:
            return "Інформація відсутня"

        if gender in ["Хлопчик", "Дівчинка"]:
            gender_key = "boy_development" if gender == "Хлопчик" else "girl_development"
            gender_info = week_data.get(gender_key, "")
            if gender_info:
                return gender_info

        return week_data.get("baby_development", "Інформація відсутня")

    def get_mother_changes_info(self, week):
        return self._get_week_info(week, "mother_changes")

    def get_nutrition_tips(self, week):
        return self._get_week_info(week, "nutrition_tips")

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