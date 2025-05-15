from datetime import datetime, timedelta

class PregnancyData:
    """Клас для зберігання та обчислення даних про вагітність"""
    
    def __init__(self):
        self.due_date = None  # Очікувана дата пологів
        self.last_period_date = None  # Дата останньої менструації
        self.conception_date = None  # Дата зачаття (якщо відома)
        self.baby_gender = "Невідомо"  # Стать дитини
        self.baby_name = ""  # Ім'я дитини (якщо вибране)
    
    def set_due_date(self, due_date):
        """Встановити очікувану дату пологів"""
        self.due_date = due_date
        
        # Розрахунок дати останньої менструації (приблизно 40 тижнів до пологів)
        if due_date:
            self.last_period_date = due_date - timedelta(days=280)
    
    def set_last_period_date(self, last_period_date):
        """Встановити дату останньої менструації і розрахувати очікувану дату пологів"""
        self.last_period_date = last_period_date
        
        # Розрахунок очікуваної дати пологів (приблизно через 40 тижнів)
        if last_period_date:
            self.due_date = last_period_date + timedelta(days=280)
    
    def set_conception_date(self, conception_date):
        """Встановити дату зачаття і розрахувати очікувану дату пологів"""
        self.conception_date = conception_date
        
        # Розрахунок очікуваної дати пологів (приблизно через 38 тижнів від зачаття)
        if conception_date:
            self.due_date = conception_date + timedelta(days=266)
            
            # Приблизна дата останньої менструації (2 тижні до зачаття)
            self.last_period_date = conception_date - timedelta(days=14)
    
    def get_current_week(self):
        """Повертає поточний акушерський тиждень вагітності"""
        if self.last_period_date:
            days_pregnant = (datetime.now().date() - self.last_period_date).days
            weeks = days_pregnant // 7
            return max(1, min(weeks, 42))  # Обмежуємо між 1 і 42 тижнями
        return None
    
    def get_days_left(self):
        """Повертає кількість днів до очікуваної дати пологів"""
        if self.due_date:
            days_left = (self.due_date - datetime.now().date()).days
            return max(0, days_left)  # Не показуємо від'ємні дні
        return None
    
    def get_trimester(self):
        """Повертає поточний триместр"""
        week = self.get_current_week()
        if week is None:
            return None
        
        if week <= 13:
            return 1
        elif week <= 27:
            return 2
        else:
            return 3
            
    def to_dict(self):
        """Повертає дані у вигляді словника для серіалізації"""
        return {
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'last_period_date': self.last_period_date.isoformat() if self.last_period_date else None,
            'conception_date': self.conception_date.isoformat() if self.conception_date else None,
            'baby_gender': self.baby_gender,
            'baby_name': self.baby_name
        }
        
    @classmethod
    def from_dict(cls, data):
        """Створює екземпляр класу з словника"""
        pregnancy = cls()
        
        if data.get('due_date'):
            pregnancy.due_date = datetime.fromisoformat(data['due_date']).date()
            
        if data.get('last_period_date'):
            pregnancy.last_period_date = datetime.fromisoformat(data['last_period_date']).date()
            
        if data.get('conception_date'):
            pregnancy.conception_date = datetime.fromisoformat(data['conception_date']).date()
            
        pregnancy.baby_gender = data.get('baby_gender', "Невідомо")
        pregnancy.baby_name = data.get('baby_name', "")
        
        return pregnancy 