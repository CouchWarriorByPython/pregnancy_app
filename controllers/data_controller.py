from models.database import Database
from models.services import PregnancyService
from utils.logger import get_logger

logger = get_logger('data_controller')


class DataController:
    def __init__(self, user_id=None):
        logger.info(f"Ініціалізація DataController для user_id: {user_id}")
        self.user_id = user_id
        self.db = Database()
        self.user_profile = None
        self.pregnancy_data = None

        if user_id:
            self._load_user_data()
        else:
            logger.warning("DataController ініціалізовано без user_id")

    def _load_user_data(self):
        """Завантажує дані користувача з бази"""
        try:
            self.user_profile = self.db.get_user_profile(self.user_id)
            if not self.user_profile:
                logger.error(f"Користувач з ID {self.user_id} не знайдений")
                return

            self.pregnancy_data = self.db.get_pregnancy_data(self.user_id)
            if not self.pregnancy_data:
                logger.info(f"Дані про вагітність не знайдені для користувача {self.user_id}, створюємо нові")
                self.pregnancy_data = self.db.create_pregnancy_data(self.user_id)

            logger.info(f"Дані користувача {self.user_profile.name} успішно завантажені")
        except Exception as e:
            logger.error(f"Помилка завантаження даних користувача {self.user_id}: {str(e)}")

    def get_current_week(self):
        """Отримує поточний тиждень вагітності"""
        if not self.user_id:
            logger.warning("Неможливо отримати поточний тиждень без user_id, повертаємо демо значення")
            return 33

        if self.pregnancy_data and self.pregnancy_data.last_period_date:
            week = PregnancyService.calculate_current_week(self.pregnancy_data.last_period_date)
            logger.info(f"Поточний тиждень вагітності для користувача {self.user_id}: {week}")
            return week

        logger.warning(f"Не вдалося розрахувати тиждень для користувача {self.user_id}, повертаємо демо значення")
        return 33

    def get_days_left(self):
        """Отримує кількість днів до пологів"""
        if not self.user_id or not self.pregnancy_data:
            return None

        due_date = self.pregnancy_data.due_date
        if due_date:
            days = PregnancyService.calculate_days_left(due_date)
            logger.info(f"Днів до пологів для користувача {self.user_id}: {days}")
            return days
        return None

    def save_user_profile(self):
        """Зберігає профіль користувача"""
        if not self.user_id or not self.user_profile:
            logger.error("Неможливо зберегти профіль без user_id або user_profile")
            return False

        try:
            logger.info(f"Збереження профілю користувача: {self.user_profile.name}")
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Помилка збереження профілю користувача {self.user_id}: {str(e)}")
            return False

    def save_pregnancy_data(self):
        """Зберігає дані про вагітність"""
        if not self.user_id or not self.pregnancy_data:
            logger.error("Неможливо зберегти дані про вагітність без user_id або pregnancy_data")
            return False

        try:
            logger.info(f"Збереження даних про вагітність для користувача {self.user_id}")
            self.db.commit()
            return True
        except Exception as e:
            logger.error(f"Помилка збереження даних про вагітність для користувача {self.user_id}: {str(e)}")
            return False

    def save_child_info(self, child_data):
        """Зберігає інформацію про дитину"""
        if not self.user_id or not self.pregnancy_data:
            logger.error("Неможливо зберегти інформацію про дитину без user_id або pregnancy_data")
            return False

        try:
            logger.info(f"Збереження інформації про дитину для користувача {self.user_id}: {child_data}")

            self.pregnancy_data.baby_gender = child_data.get('gender', 'Невідомо')
            self.pregnancy_data.baby_name = child_data.get('name', '')

            if 'first_labour' in child_data and self.user_profile:
                self.user_profile.previous_pregnancies = 0 if child_data['first_labour'] else 1

            self.db.commit()

            # Перезавантажуємо дані після збереження
            self._load_user_data()
            return True
        except Exception as e:
            logger.error(f"Помилка збереження інформації про дитину для користувача {self.user_id}: {str(e)}")
            return False

    def is_first_launch(self):
        """Перевіряє чи це перший запуск для користувача"""
        if not self.user_id or not self.user_profile or not self.pregnancy_data:
            logger.info("Перший запуск: відсутні базові дані користувача")
            return True

        try:
            # Перевіряємо чи є інформація про дитину
            has_child_info = (self.pregnancy_data.baby_gender and
                              self.pregnancy_data.baby_gender != "Невідомо")

            # Перевіряємо чи є інформація про користувача
            has_user_info = (self.user_profile.name and
                             self.user_profile.name.strip() and
                             self.user_profile.name != "Користувач")

            # Перевіряємо чи є інформація про вагітність
            has_pregnancy_info = self.pregnancy_data.last_period_date is not None

            is_first = not (has_child_info and has_user_info and has_pregnancy_info)
            logger.info(f"Перевірка першого запуску для користувача {self.user_id}: "
                        f"child_info={has_child_info}, user_info={has_user_info}, "
                        f"pregnancy_info={has_pregnancy_info}, is_first={is_first}")
            return is_first
        except Exception as e:
            logger.error(f"Помилка при перевірці першого запуску для користувача {self.user_id}: {str(e)}")
            return True

    def get_child_info(self):
        """Отримує інформацію про дитину"""
        if not self.pregnancy_data or not self.user_profile:
            logger.warning("Відсутні дані для отримання інформації про дитину, повертаємо дефолтні значення")
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

    def is_logged_in(self):
        """Перевіряє чи користувач авторизований"""
        return self.user_id is not None and self.user_profile is not None

    def refresh_data(self):
        """Перезавантажує дані з бази"""
        if self.user_id:
            self._load_user_data()
        else:
            logger.warning("Неможливо перезавантажити дані без user_id")