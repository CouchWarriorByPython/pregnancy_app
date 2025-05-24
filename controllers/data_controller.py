from models.database import Database
from models.services import PregnancyService
from utils.logger import get_logger

logger = get_logger('data_controller')


class DataController:
    def __init__(self, user_id=None):
        logger.info("Ініціалізація DataController")
        self.user_id = user_id
        self.db = Database()

        if user_id:
            self.user_profile = self.db.get_user_profile(user_id)
            self.pregnancy_data = self.db.get_pregnancy_data(user_id)
        else:
            # Створюємо тимчасові об'єкти для неавторизованих користувачів
            self.user_profile = type('obj', (object,), {
                'name': 'Користувач',
                'email': '',
                'weight_before_pregnancy': 60.0,
                'height': 165,
                'previous_pregnancies': 0,
                'cycle_length': 28
            })
            self.pregnancy_data = self.db.get_pregnancy_data(1)  # Використовуємо демо-дані

    def get_current_week(self):
        if self.pregnancy_data and self.pregnancy_data.last_period_date:
            week = PregnancyService.calculate_current_week(self.pregnancy_data.last_period_date)
            logger.info(f"Поточний тиждень вагітності: {week}")
            return week
        return 33  # Дефолтне значення для демо

    def get_days_left(self):
        if self.pregnancy_data:
            due_date = self.pregnancy_data.due_date
            if due_date:
                days = PregnancyService.calculate_days_left(due_date)
                logger.info(f"Днів до пологів: {days}")
                return days
        return None

    def save_user_profile(self):
        if self.user_profile:
            logger.info(f"Збереження профілю користувача: {self.user_profile.name}")
            self.db.commit()

    def save_pregnancy_data(self):
        if self.pregnancy_data:
            logger.info("Збереження даних про вагітність")
            self.db.commit()

    def save_child_info(self, child_data):
        if not self.pregnancy_data:
            return False

        logger.info(f"Збереження інформації про дитину: {child_data}")
        self.pregnancy_data.baby_gender = child_data.get('gender', 'Невідомо')
        self.pregnancy_data.baby_name = child_data.get('name', '')

        if 'first_labour' in child_data and self.user_profile:
            self.user_profile.previous_pregnancies = 0 if child_data['first_labour'] else 1

        self.db.commit()
        if self.user_id:
            self.pregnancy_data = self.db.get_pregnancy_data(self.user_id)
            self.user_profile = self.db.get_user_profile(self.user_id)
        return True

    def is_first_launch(self):
        if not self.user_profile or not self.pregnancy_data:
            return True

        try:
            has_child_info = (self.pregnancy_data.baby_gender and
                              self.pregnancy_data.baby_gender != "Невідомо")
            has_user_info = (self.user_profile.name and
                             self.user_profile.name.strip() and
                             self.user_profile.name != "Користувач")
            has_pregnancy_info = self.pregnancy_data.last_period_date is not None

            is_first = not (has_child_info and has_user_info and has_pregnancy_info)
            logger.info(f"Перевірка першого запуску: is_first={is_first}")
            return is_first
        except Exception as e:
            logger.error(f"Помилка при перевірці першого запуску: {str(e)}")
            return True

    def get_child_info(self):
        if not self.pregnancy_data or not self.user_profile:
            return {
                "name": "",
                "gender": "Невідомо",
                "first_labour": True
            }

        return {
            "name": self.pregnancy_data.baby_name or "",
            "gender": self.pregnancy_data.baby_gender or "Невідомо",
            "first_labour": self.user_profile.previous_pregnancies == 0
        }