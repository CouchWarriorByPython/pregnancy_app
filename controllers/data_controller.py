from models.database import Database
from models.services import PregnancyService
from utils.logger import get_logger

logger = get_logger('data_controller')


class DataController:
    def __init__(self):
        logger.info("Ініціалізація DataController")
        self.db = Database()
        self.user_profile = self.db.get_user_profile()
        self.pregnancy_data = self.db.get_pregnancy_data()

    def get_current_week(self):
        if self.pregnancy_data and self.pregnancy_data.last_period_date:
            week = PregnancyService.calculate_current_week(self.pregnancy_data.last_period_date)
            logger.info(f"Поточний тиждень вагітності: {week}")
            return week
        return None

    def get_days_left(self):
        if self.pregnancy_data and self.pregnancy_data.due_date:
            days = PregnancyService.calculate_days_left(self.pregnancy_data.due_date)
            logger.info(f"Днів до пологів: {days}")
            return days
        return None

    def save_user_profile(self):
        logger.info(f"Збереження профілю користувача: {self.user_profile.name}")
        self.db.commit()
        logger.info("Профіль користувача збережено")

    def save_pregnancy_data(self):
        logger.info("Збереження даних про вагітність")

        if self.pregnancy_data.last_period_date and not self.pregnancy_data.due_date:
            self.pregnancy_data.due_date = PregnancyService.calculate_due_date_from_lmp(
                self.pregnancy_data.last_period_date)

        self.db.commit()
        logger.info("Дані про вагітність збережено")

    def save_child_info(self, child_data):
        logger.info(f"Збереження інформації про дитину: {child_data}")

        self.pregnancy_data.baby_gender = child_data.get('gender', 'Невідомо')
        self.pregnancy_data.baby_name = child_data.get('name', '')

        if 'first_labour' in child_data:
            self.user_profile.previous_pregnancies = 0 if child_data['first_labour'] else 1

        self.db.commit()
        return True

    def is_first_launch(self):
        try:
            return (not self.pregnancy_data.baby_gender or
                    self.pregnancy_data.baby_gender == "Невідомо")
        except Exception as e:
            logger.error(f"Помилка при перевірці першого запуску: {str(e)}")
            return True

    def get_child_info(self):
        return {
            "name": self.pregnancy_data.baby_name or "",
            "gender": self.pregnancy_data.baby_gender or "Невідомо",
            "first_labour": self.user_profile.previous_pregnancies == 0
        }