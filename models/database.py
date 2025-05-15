import sqlite3
import logging
import os
from datetime import datetime

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

logger = logging.getLogger('database')

class Database:
    def __init__(self, db_path='pregnancy_diary.db'):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Ініціалізація бази даних і створення таблиць"""
        logger.info(f"Ініціалізація бази даних: {self.db_path}")
        
        # Перевіряємо, чи існує файл БД
        db_exists = os.path.exists(self.db_path)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Створюємо таблиці, якщо їх немає
        if not db_exists:
            logger.info("Створення структури бази даних")
            
            # Таблиця для профілю користувача
            c.execute('''
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    birth_date TEXT,
                    height INTEGER,
                    weight_before_pregnancy REAL,
                    previous_pregnancies INTEGER,
                    cycle_length INTEGER
                )
            ''')
            
            # Таблиця для дієтичних вподобань
            c.execute('''
                CREATE TABLE IF NOT EXISTS diet_preferences (
                    id INTEGER PRIMARY KEY,
                    preference TEXT
                )
            ''')
            
            # Таблиця для даних про вагітність
            c.execute('''
                CREATE TABLE IF NOT EXISTS pregnancy_data (
                    id INTEGER PRIMARY KEY,
                    last_period_date TEXT,
                    due_date TEXT,
                    conception_date TEXT,
                    baby_gender TEXT,
                    baby_name TEXT
                )
            ''')
            
            # Таблиця для записів ваги
            c.execute('''
                CREATE TABLE IF NOT EXISTS weight_records (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    weight REAL
                )
            ''')
            
            # Таблиця для подій у календарі
            c.execute('''
                CREATE TABLE IF NOT EXISTS calendar_events (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    all_day BOOLEAN,
                    reminder BOOLEAN,
                    reminder_time TEXT,
                    event_type TEXT
                )
            ''')
            
            # Таблиця для чекліста медичних обстежень
            c.execute('''
                CREATE TABLE IF NOT EXISTS medical_checks (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    trimester INTEGER,
                    is_completed BOOLEAN,
                    completion_date TEXT,
                    is_custom BOOLEAN
                )
            ''')
            
            # Таблиця для списку бажань
            c.execute('''
                CREATE TABLE IF NOT EXISTS wishlist (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    category TEXT,
                    price REAL,
                    is_purchased BOOLEAN,
                    purchase_date TEXT,
                    priority INTEGER
                )
            ''')
            
            # Додаємо початкові дані для профілю
            c.execute('''
                INSERT INTO user_profile (id, name, birth_date, height, weight_before_pregnancy, previous_pregnancies, cycle_length) 
                VALUES (1, 'Користувач', NULL, 165, 60.0, 0, 28)
            ''')
            
            # Додаємо початкові дані для вагітності
            today = datetime.now().strftime('%Y-%m-%d')
            due_date = (datetime.now().replace(year=datetime.now().year + 1)).strftime('%Y-%m-%d')
            
            c.execute('''
                INSERT INTO pregnancy_data (id, last_period_date, due_date, conception_date, baby_gender, baby_name) 
                VALUES (1, ?, ?, NULL, 'Невідомо', '')
            ''', (today, due_date))
            
            conn.commit()
            logger.info("Структура бази даних створена успішно")
        
        conn.close()
    
    def get_connection(self):
        """Повертає з'єднання з базою даних"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query, params=()):
        """Виконує SQL запит та повертає результат"""
        logger.debug(f"SQL запит: {query} з параметрами: {params}")
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(query, params)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result
    
    def execute_insert(self, query, params=()):
        """Виконує SQL запит вставки та повертає ID вставленого запису"""
        logger.debug(f"SQL вставка: {query} з параметрами: {params}")
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(query, params)
        last_id = c.lastrowid
        conn.commit()
        conn.close()
        return last_id
    
    def execute_update(self, query, params=()):
        """Виконує SQL запит оновлення та повертає кількість змінених рядків"""
        logger.debug(f"SQL оновлення: {query} з параметрами: {params}")
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(query, params)
        rows_affected = c.rowcount
        conn.commit()
        conn.close()
        return rows_affected
    
    # Методи для роботи з профілем користувача
    def get_user_profile(self):
        """Отримує профіль користувача"""
        logger.info("Отримання профілю користувача")
        result = self.execute_query("SELECT * FROM user_profile WHERE id = 1")
        if result:
            return {
                'id': result[0][0],
                'name': result[0][1],
                'birth_date': result[0][2],
                'height': result[0][3],
                'weight_before_pregnancy': result[0][4],
                'previous_pregnancies': result[0][5],
                'cycle_length': result[0][6]
            }
        return None
        
    def update_user_profile(self, name, birth_date, height, weight_before_pregnancy, previous_pregnancies, cycle_length):
        """Оновлює профіль користувача"""
        logger.info(f"Оновлення профілю користувача: {name}")
        return self.execute_update(
            "UPDATE user_profile SET name=?, birth_date=?, height=?, weight_before_pregnancy=?, previous_pregnancies=?, cycle_length=? WHERE id=1",
            (name, birth_date, height, weight_before_pregnancy, previous_pregnancies, cycle_length)
        )
    
    # Методи для роботи з дієтичними вподобаннями
    def get_diet_preferences(self):
        """Отримує список дієтичних вподобань"""
        logger.info("Отримання дієтичних вподобань")
        result = self.execute_query("SELECT preference FROM diet_preferences")
        return [row[0] for row in result]
        
    def update_diet_preferences(self, preferences):
        """Оновлює список дієтичних вподобань"""
        logger.info(f"Оновлення дієтичних вподобань: {preferences}")
        # Спочатку видаляємо всі поточні записи
        self.execute_update("DELETE FROM diet_preferences")
        
        # Додаємо нові записи
        for pref in preferences:
            self.execute_insert("INSERT INTO diet_preferences (preference) VALUES (?)", (pref,))
    
    # Методи для роботи з даними про вагітність
    def get_pregnancy_data(self):
        """Отримує дані про вагітність"""
        logger.info("Отримання даних про вагітність")
        result = self.execute_query("SELECT * FROM pregnancy_data WHERE id = 1")
        if result:
            return {
                'id': result[0][0],
                'last_period_date': result[0][1],
                'due_date': result[0][2],
                'conception_date': result[0][3],
                'baby_gender': result[0][4],
                'baby_name': result[0][5]
            }
        return None
        
    def update_pregnancy_data(self, last_period_date, due_date, conception_date, baby_gender, baby_name):
        """Оновлює дані про вагітність"""
        logger.info("Оновлення даних про вагітність")
        return self.execute_update(
            "UPDATE pregnancy_data SET last_period_date=?, due_date=?, conception_date=?, baby_gender=?, baby_name=? WHERE id=1",
            (last_period_date, due_date, conception_date, baby_gender, baby_name)
        )
    
    # Методи для роботи з вагою
    def add_weight_record(self, date, weight):
        """Додає новий запис про вагу"""
        logger.info(f"Додавання запису про вагу: {weight} кг на дату {date}")
        return self.execute_insert(
            "INSERT INTO weight_records (date, weight) VALUES (?, ?)",
            (date, weight)
        )
        
    def get_weight_records(self):
        """Отримує всі записи про вагу"""
        logger.info("Отримання записів про вагу")
        result = self.execute_query("SELECT date, weight FROM weight_records ORDER BY date")
        return [(row[0], row[1]) for row in result]
    
    # Методи для роботи з календарем подій
    def add_calendar_event(self, title, description, start_date, end_date, all_day=False, reminder=False, reminder_time=None, event_type='regular'):
        """Додає нову подію до календаря"""
        logger.info(f"Додавання події до календаря: {title} на дату {start_date}")
        return self.execute_insert(
            "INSERT INTO calendar_events (title, description, start_date, end_date, all_day, reminder, reminder_time, event_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (title, description, start_date, end_date, all_day, reminder, reminder_time, event_type)
        )
        
    def get_calendar_events(self, start_date=None, end_date=None):
        """Отримує події з календаря у вказаному діапазоні дат"""
        logger.info(f"Отримання подій календаря між {start_date} і {end_date}")
        query = "SELECT * FROM calendar_events"
        params = []
        
        if start_date and end_date:
            query += " WHERE start_date >= ? AND end_date <= ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " WHERE start_date >= ?"
            params.append(start_date)
        elif end_date:
            query += " WHERE end_date <= ?"
            params.append(end_date)
        
        result = self.execute_query(query, tuple(params))
        events = []
        for row in result:
            events.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'start_date': row[3],
                'end_date': row[4],
                'all_day': bool(row[5]),
                'reminder': bool(row[6]),
                'reminder_time': row[7],
                'event_type': row[8]
            })
        return events
    
    # Методи для роботи з чеклістом медичних обстежень
    def add_medical_check(self, title, description, trimester, is_custom=False):
        """Додає новий пункт до чекліста медичних обстежень"""
        logger.info(f"Додавання медичного обстеження: {title} для триместру {trimester}")
        return self.execute_insert(
            "INSERT INTO medical_checks (title, description, trimester, is_completed, is_custom) VALUES (?, ?, ?, 0, ?)",
            (title, description, trimester, is_custom)
        )
        
    def get_medical_checks_by_trimester(self, trimester):
        """Отримує список медичних обстежень для вказаного триместру"""
        logger.info(f"Отримання медичних обстежень для триместру {trimester}")
        result = self.execute_query(
            "SELECT * FROM medical_checks WHERE trimester = ?",
            (trimester,)
        )
        checks = []
        for row in result:
            checks.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'trimester': row[3],
                'is_completed': bool(row[4]),
                'completion_date': row[5],
                'is_custom': bool(row[6])
            })
        return checks
        
    def complete_medical_check(self, check_id, completion_date=None):
        """Позначає медичне обстеження як виконане"""
        if not completion_date:
            completion_date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"Позначення медичного обстеження {check_id} як виконаного")
        return self.execute_update(
            "UPDATE medical_checks SET is_completed = 1, completion_date = ? WHERE id = ?",
            (completion_date, check_id)
        )
    
    # Методи для роботи зі списком бажань
    def add_wishlist_item(self, title, description, category, price=None, priority=3):
        """Додає новий товар до списку бажань"""
        logger.info(f"Додавання товару до списку бажань: {title}")
        return self.execute_insert(
            "INSERT INTO wishlist (title, description, category, price, is_purchased, priority) VALUES (?, ?, ?, ?, 0, ?)",
            (title, description, category, price, priority)
        )
        
    def get_wishlist_items(self, category=None):
        """Отримує товари зі списку бажань, можливо за категорією"""
        logger.info(f"Отримання товарів зі списку бажань (категорія: {category})")
        query = "SELECT * FROM wishlist"
        params = []
        
        if category:
            query += " WHERE category = ?"
            params.append(category)
        
        result = self.execute_query(query, tuple(params))
        items = []
        for row in result:
            items.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'category': row[3],
                'price': row[4],
                'is_purchased': bool(row[5]),
                'purchase_date': row[6],
                'priority': row[7]
            })
        return items
        
    def mark_wishlist_item_purchased(self, item_id, purchase_date=None):
        """Позначає товар зі списку бажань як придбаний"""
        if not purchase_date:
            purchase_date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"Позначення товару {item_id} як придбаного")
        return self.execute_update(
            "UPDATE wishlist SET is_purchased = 1, purchase_date = ? WHERE id = ?",
            (purchase_date, item_id)
        ) 