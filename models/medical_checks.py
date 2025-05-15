from datetime import datetime

class MedicalCheck:
    """Клас для представлення медичного обстеження або аналізу"""
    
    def __init__(self, check_id=None, title="", description="", type_category="", 
                 recommended_week=None, deadline_week=None, is_completed=False):
        self.check_id = check_id or f"check_{int(datetime.now().timestamp())}"
        self.title = title  # Назва обстеження
        self.description = description  # Опис або рекомендації
        self.type_category = type_category  # Категорія (аналізи, УЗД, консультації...)
        self.recommended_week = recommended_week  # Рекомендований тиждень для проходження
        self.deadline_week = deadline_week  # Крайній тиждень для проходження
        self.is_completed = is_completed  # Статус виконання
        self.completion_date = None  # Дата виконання
        self.notes = ""  # Нотатки користувача
    
    def mark_as_completed(self):
        """Позначити обстеження як виконане"""
        self.is_completed = True
        self.completion_date = datetime.now().date()
    
    def to_dict(self):
        """Повертає дані у вигляді словника для серіалізації"""
        return {
            'check_id': self.check_id,
            'title': self.title,
            'description': self.description,
            'type_category': self.type_category,
            'recommended_week': self.recommended_week,
            'deadline_week': self.deadline_week,
            'is_completed': self.is_completed,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        """Створює екземпляр класу з словника"""
        check = cls(
            check_id=data.get('check_id'),
            title=data.get('title', ""),
            description=data.get('description', ""),
            type_category=data.get('type_category', ""),
            recommended_week=data.get('recommended_week'),
            deadline_week=data.get('deadline_week'),
            is_completed=data.get('is_completed', False)
        )
        
        if data.get('completion_date'):
            check.completion_date = datetime.fromisoformat(data['completion_date']).date()
            
        check.notes = data.get('notes', "")
        
        return check


class ChecklistManager:
    """Клас для управління списками медичних обстежень"""
    
    def __init__(self):
        self.checklists = {
            1: [],  # Перший триместр
            2: [],  # Другий триместр
            3: []   # Третій триместр
        }
        self.load_default_checklists()
    
    def load_default_checklists(self):
        """Завантажує стандартні чекліти для кожного триместру"""
        # Перший триместр
        first_trimester = [
            MedicalCheck(title="Загальний аналіз крові", description="До 12 тижнів", 
                        type_category="Аналізи", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Аналіз крові на групу та резус-фактор", 
                        description="До 12 тижнів", type_category="Аналізи", 
                        recommended_week=8, deadline_week=12),
            MedicalCheck(title="Аналіз крові на ВІЛ", description="До 12 тижнів", 
                        type_category="Аналізи", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Аналіз крові на сифіліс", description="До 12 тижнів", 
                        type_category="Аналізи", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Загальний аналіз сечі", description="До 12 тижнів", 
                        type_category="Аналізи", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Аналіз на TORCH-інфекції", description="До 12 тижнів", 
                        type_category="Аналізи", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Перше скринінгове УЗД", description="11-13 тижнів", 
                        type_category="УЗД", recommended_week=11, deadline_week=13),
            MedicalCheck(title="Гінеколог", description="Перший візит до 12 тижнів", 
                        type_category="Консультації", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Терапевт", description="До 12 тижнів", 
                        type_category="Консультації", recommended_week=8, deadline_week=12),
            MedicalCheck(title="Стоматолог", description="До 12 тижнів", 
                        type_category="Консультації", recommended_week=8, deadline_week=12),
        ]
        self.checklists[1] = first_trimester
        
        # Другий триместр
        second_trimester = [
            MedicalCheck(title="Загальний аналіз крові", description="16-20 тижнів", 
                        type_category="Аналізи", recommended_week=16, deadline_week=20),
            MedicalCheck(title="Загальний аналіз сечі", description="16-20 тижнів", 
                        type_category="Аналізи", recommended_week=16, deadline_week=20),
            MedicalCheck(title="Глюкозотолерантний тест", description="24-28 тижнів", 
                        type_category="Аналізи", recommended_week=24, deadline_week=28),
            MedicalCheck(title="Друге скринінгове УЗД", description="18-22 тижнів", 
                        type_category="УЗД", recommended_week=18, deadline_week=22),
            MedicalCheck(title="Гінеколог", description="Кожні 4 тижні", 
                        type_category="Консультації", recommended_week=16, deadline_week=20),
            MedicalCheck(title="Окуліст", description="До 20 тижнів", 
                        type_category="Консультації", recommended_week=16, deadline_week=20),
        ]
        self.checklists[2] = second_trimester
        
        # Третій триместр
        third_trimester = [
            MedicalCheck(title="Загальний аналіз крові", description="30 тижнів", 
                        type_category="Аналізи", recommended_week=30, deadline_week=32),
            MedicalCheck(title="Загальний аналіз сечі", description="30-32 тижнів", 
                        type_category="Аналізи", recommended_week=30, deadline_week=32),
            MedicalCheck(title="Аналіз крові на ВІЛ", description="30 тижнів", 
                        type_category="Аналізи", recommended_week=30, deadline_week=32),
            MedicalCheck(title="Аналіз крові на сифіліс", description="30 тижнів", 
                        type_category="Аналізи", recommended_week=30, deadline_week=32),
            MedicalCheck(title="Мазок на флору", description="30 тижнів", 
                        type_category="Аналізи", recommended_week=30, deadline_week=32),
            MedicalCheck(title="Третє скринінгове УЗД", description="32-34 тижнів", 
                        type_category="УЗД", recommended_week=32, deadline_week=34),
            MedicalCheck(title="Доплерометрія", description="34-36 тижнів", 
                        type_category="УЗД", recommended_week=34, deadline_week=36),
            MedicalCheck(title="Гінеколог", description="Кожні 2 тижні до 36 тижня, потім щотижня", 
                        type_category="Консультації", recommended_week=28, deadline_week=40),
            MedicalCheck(title="Консультація анестезіолога", description="За 2-3 тижні до пологів", 
                        type_category="Консультації", recommended_week=37, deadline_week=38),
        ]
        self.checklists[3] = third_trimester
    
    def get_checklist_for_trimester(self, trimester):
        """Отримує чекліст для конкретного триместру"""
        if trimester in self.checklists:
            return self.checklists[trimester]
        return []
    
    def get_progress_for_trimester(self, trimester):
        """Повертає прогрес виконання чекліста для триместру"""
        if trimester not in self.checklists or not self.checklists[trimester]:
            return 0
            
        completed = sum(1 for check in self.checklists[trimester] if check.is_completed)
        total = len(self.checklists[trimester])
        
        if total == 0:
            return 0
            
        return int((completed / total) * 100)
    
    def add_custom_check(self, check, trimester):
        """Додає користувацьке обстеження до чекліста"""
        if trimester in self.checklists:
            self.checklists[trimester].append(check)
    
    def get_upcoming_checks(self, current_week):
        """Повертає список найближчих обстежень"""
        upcoming = []
        
        for trimester, checks in self.checklists.items():
            for check in checks:
                if not check.is_completed and check.recommended_week:
                    if check.recommended_week >= current_week and check.recommended_week <= current_week + 4:
                        upcoming.append(check)
        
        # Сортуємо за рекомендованим тижнем
        upcoming.sort(key=lambda x: x.recommended_week)
        return upcoming
    
    def get_overdue_checks(self, current_week):
        """Повертає список прострочених обстежень"""
        overdue = []
        
        for trimester, checks in self.checklists.items():
            for check in checks:
                if not check.is_completed and check.deadline_week:
                    if check.deadline_week < current_week:
                        overdue.append(check)
        
        return overdue
    
    def mark_check_as_completed(self, check_id):
        """Позначає обстеження як виконане за його ID"""
        for trimester, checks in self.checklists.items():
            for check in checks:
                if check.check_id == check_id:
                    check.mark_as_completed()
                    return True
        return False
    
    def to_dict(self):
        """Повертає дані у вигляді словника для серіалізації"""
        return {
            str(trimester): [check.to_dict() for check in checks]
            for trimester, checks in self.checklists.items()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Створює екземпляр класу з словника"""
        manager = cls()
        
        # Очищаємо стандартні чекліти
        manager.checklists = {1: [], 2: [], 3: []}
        
        # Заповнюємо з даних
        for trimester_str, checks_data in data.items():
            trimester = int(trimester_str)
            checks = [MedicalCheck.from_dict(check_data) for check_data in checks_data]
            manager.checklists[trimester] = checks
        
        return manager 