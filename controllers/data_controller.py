from datetime import date
from models.database import Database
from utils.logger import get_logger

logger = get_logger('data_controller')


class UserProfile:
    def __init__(self):
        self.id = 1
        self.name = "Користувач"
        self.birth_date = None
        self.height = 165
        self.weight_before_pregnancy = 60.0
        self.previous_pregnancies = 0
        self.cycle_length = 28
        self.diet_preferences = []


class PregnancyData:
    def __init__(self):
        self.id = 1
        self.last_period_date = None
        self.due_date = None
        self.conception_date = None
        self.baby_gender = "Невідомо"
        self.baby_name = ""


class DataController:
    """Контролер для управління даними додатку"""

    def __init__(self):
        logger.info("Ініціалізація DataController")
        self.db = Database()
        self.user_profile = UserProfile()
        self.pregnancy_data = PregnancyData()
        self.load_data()

    def load_data(self):
        logger.info("Завантаження даних з бази")
        self._load_user_profile()
        self._load_pregnancy_data()

    def _load_user_profile(self):
        profile_data = self.db.get_user_profile()
        if profile_data:
            self.user_profile.id = profile_data['id']
            self.user_profile.name = profile_data['name']

            if profile_data['birth_date']:
                try:
                    birth_parts = profile_data['birth_date'].split('-')
                    self.user_profile.birth_date = date(int(birth_parts[0]), int(birth_parts[1]), int(birth_parts[2]))
                except Exception as e:
                    logger.error(f"Помилка перетворення дати народження: {e}")

            self.user_profile.height = profile_data['height']
            self.user_profile.weight_before_pregnancy = profile_data['weight_before_pregnancy']
            self.user_profile.previous_pregnancies = profile_data['previous_pregnancies']
            self.user_profile.cycle_length = profile_data['cycle_length']

            self.user_profile.diet_preferences = self.db.get_diet_preferences()

            logger.info(f"Завантажено профіль користувача: {self.user_profile.name}")

    def _load_pregnancy_data(self):
        pregnancy_data = self.db.get_pregnancy_data()
        if pregnancy_data:
            self.pregnancy_data.id = pregnancy_data['id']

            if pregnancy_data['last_period_date']:
                try:
                    date_parts = pregnancy_data['last_period_date'].split('-')
                    self.pregnancy_data.last_period_date = date(int(date_parts[0]), int(date_parts[1]),
                                                                int(date_parts[2]))
                except Exception as e:
                    logger.error(f"Помилка перетворення дати останньої менструації: {e}")

            if pregnancy_data['due_date']:
                try:
                    date_parts = pregnancy_data['due_date'].split('-')
                    self.pregnancy_data.due_date = date(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
                except Exception as e:
                    logger.error(f"Помилка перетворення очікуваної дати пологів: {e}")

            if pregnancy_data['conception_date']:
                try:
                    date_parts = pregnancy_data['conception_date'].split('-')
                    self.pregnancy_data.conception_date = date(int(date_parts[0]), int(date_parts[1]),
                                                               int(date_parts[2]))
                except Exception as e:
                    logger.error(f"Помилка перетворення дати зачаття: {e}")

            self.pregnancy_data.baby_gender = pregnancy_data['baby_gender']
            self.pregnancy_data.baby_name = pregnancy_data['baby_name']

            logger.info("Завантажено дані про вагітність")

    def save_user_profile(self):
        logger.info(f"Збереження профілю користувача: {self.user_profile.name}")

        birth_date_str = None
        if self.user_profile.birth_date:
            birth_date_str = self.user_profile.birth_date.strftime("%Y-%m-%d")

        self.db.update_user_profile(
            self.user_profile.name,
            birth_date_str,
            self.user_profile.height,
            self.user_profile.weight_before_pregnancy,
            self.user_profile.previous_pregnancies,
            self.user_profile.cycle_length
        )

        self.db.update_diet_preferences(self.user_profile.diet_preferences)

        logger.info("Профіль користувача збережено")

    def save_pregnancy_data(self):
        logger.info("Збереження даних про вагітність")

        last_period_str = None
        if self.pregnancy_data.last_period_date:
            last_period_str = self.pregnancy_data.last_period_date.strftime("%Y-%m-%d")

        due_date_str = None
        if self.pregnancy_data.due_date:
            due_date_str = self.pregnancy_data.due_date.strftime("%Y-%m-%d")

        conception_date_str = None
        if self.pregnancy_data.conception_date:
            conception_date_str = self.pregnancy_data.conception_date.strftime("%Y-%m-%d")

        self.db.update_pregnancy_data(
            last_period_str,
            due_date_str,
            conception_date_str,
            self.pregnancy_data.baby_gender,
            self.pregnancy_data.baby_name
        )

        logger.info("Дані про вагітність збережено")

    def get_current_week(self):
        """Розрахунок поточного тижня вагітності"""
        if self.pregnancy_data.last_period_date:
            days_passed = (date.today() - self.pregnancy_data.last_period_date).days
            weeks = days_passed // 7
            logger.info(f"Поточний тиждень вагітності: {weeks}")
            return weeks
        return None

    def get_days_left(self):
        """Розрахунок кількості днів до пологів"""
        if self.pregnancy_data.due_date:
            days_left = (self.pregnancy_data.due_date - date.today()).days
            logger.info(f"Днів до пологів: {days_left}")
            return max(0, days_left)
        return None

    def save_child_info(self, child_data):
        """Зберігає інформацію про дитину та профіль користувача"""
        logger.info(f"Збереження інформації про дитину: {child_data}")

        # Оновлюємо дані про вагітність
        self.pregnancy_data.baby_gender = child_data.get('gender', 'Невідомо')
        self.pregnancy_data.baby_name = child_data.get('name', '')

        # Оновлюємо профіль користувача
        if 'first_labour' in child_data:
            self.user_profile.previous_pregnancies = 0 if child_data['first_labour'] else 1

        # Якщо є дані користувача (з розширеного онбордингу), оновлюємо їх
        if 'user_data' in child_data:
            user_data = child_data['user_data']

            # Оновлюємо основні поля профілю
            if 'name' in user_data and user_data['name']:
                self.user_profile.name = user_data['name']

            if 'birth_date' in user_data and user_data['birth_date']:
                try:
                    self.user_profile.birth_date = date.fromisoformat(user_data['birth_date'])
                except ValueError:
                    logger.error(f"Неправильний формат дати: {user_data['birth_date']}")

            if 'weight_before_pregnancy' in user_data:
                self.user_profile.weight_before_pregnancy = user_data['weight_before_pregnancy']

            if 'height' in user_data:
                self.user_profile.height = user_data['height']

            if 'cycle_length' in user_data:
                self.user_profile.cycle_length = user_data['cycle_length']

            # Оновлюємо дієтичні вподобання
            if 'diet_preferences' in user_data:
                self.user_profile.diet_preferences = user_data['diet_preferences']

        # Зберігаємо зміни
        self.save_pregnancy_data()
        self.save_user_profile()

        return True

    def is_first_launch(self):
        """Перевіряє, чи це перший запуск додатку"""
        try:
            # Отримуємо кількість записів у таблиці даних вагітності
            result = self.db.execute_query("SELECT COUNT(*) FROM pregnancy_data")
            count = result[0][0] if result else 0

            # Перевіряємо наявність критичних даних у моделі
            data_exists = (count > 0 and
                           self.pregnancy_data.baby_gender and
                           self.pregnancy_data.baby_gender != "Невідомо")

            logger.info(f"Перевірка першого запуску: записів у БД - {count}, наявність даних - {data_exists}")

            return not data_exists
        except Exception as e:
            logger.error(f"Помилка при перевірці першого запуску: {str(e)}")
            # У випадку помилки вважаємо, що це перший запуск
            return True

    def get_child_info(self):
        """Отримує інформацію про дитину"""
        return {
            "name": self.pregnancy_data.baby_name,
            "gender": self.pregnancy_data.baby_gender,
            "first_labour": self.user_profile.previous_pregnancies == 0
        }