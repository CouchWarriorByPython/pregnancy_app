from datetime import datetime

class UserProfile:
    """Клас для зберігання інформації про користувача додатку"""
    
    def __init__(self):
        self.name = ""  # Ім'я користувача
        self.birth_date = None  # Дата народження
        self.weight_before_pregnancy = 0  # Вага до вагітності в кг
        self.height = 0  # Зріст в см
        self.previous_pregnancies = 0  # Кількість попередніх вагітностей
        self.cycle_length = 28  # Середня тривалість менструального циклу в днях
        self.diet_preferences = []  # Дієтичні вподобання (вегетаріанство, веганство тощо)
        self.priorities = []  # Пріоритетні теми для користувача
        self.theme = "dark"  # Тема додатку (стандартна темна)
        self.accent_color = "#FF8C00"  # Акцентний колір (помаранчевий за замовчуванням)
        self.notification_level = 2  # Рівень сповіщень (0-3)
    
    def calculate_age(self):
        """Розрахунок віку користувача"""
        if self.birth_date:
            today = datetime.now().date()
            age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            return age
        return None
    
    def calculate_bmi(self):
        """Розрахунок індексу маси тіла"""
        if self.height and self.weight_before_pregnancy:
            # Формула: вага (кг) / (зріст (м) ^ 2)
            height_m = self.height / 100  # Переводимо зріст в метри
            bmi = self.weight_before_pregnancy / (height_m * height_m)
            return round(bmi, 1)
        return None
    
    def is_first_pregnancy(self):
        """Перевіряє, чи це перша вагітність"""
        return self.previous_pregnancies == 0
    
    def set_theme(self, theme_name):
        """Встановлює тему додатку та відповідний акцентний колір"""
        self.theme = theme_name
        
        # Встановлюємо акцентний колір залежно від теми
        if theme_name == "dark_pink":
            self.accent_color = "#FF69B4"  # Рожевий
        elif theme_name == "dark_blue":
            self.accent_color = "#1E90FF"  # Блакитний
        else:
            self.accent_color = "#FF8C00"  # Стандартний помаранчевий
    
    def to_dict(self):
        """Повертає дані у вигляді словника для серіалізації"""
        return {
            'name': self.name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'weight_before_pregnancy': self.weight_before_pregnancy,
            'height': self.height,
            'previous_pregnancies': self.previous_pregnancies,
            'cycle_length': self.cycle_length,
            'diet_preferences': self.diet_preferences,
            'priorities': self.priorities,
            'theme': self.theme,
            'accent_color': self.accent_color,
            'notification_level': self.notification_level
        }
    
    @classmethod
    def from_dict(cls, data):
        """Створює екземпляр класу з словника"""
        profile = cls()
        
        profile.name = data.get('name', "")
        
        if data.get('birth_date'):
            profile.birth_date = datetime.fromisoformat(data['birth_date']).date()
            
        profile.weight_before_pregnancy = data.get('weight_before_pregnancy', 0)
        profile.height = data.get('height', 0)
        profile.previous_pregnancies = data.get('previous_pregnancies', 0)
        profile.cycle_length = data.get('cycle_length', 28)
        profile.diet_preferences = data.get('diet_preferences', [])
        profile.priorities = data.get('priorities', [])
        profile.theme = data.get('theme', "dark")
        profile.accent_color = data.get('accent_color', "#FF8C00")
        profile.notification_level = data.get('notification_level', 2)
        
        return profile 