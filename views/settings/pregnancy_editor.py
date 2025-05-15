from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                          QPushButton, QDateEdit, QLineEdit, QComboBox,
                          QScrollArea, QFrame, QFormLayout, QSizePolicy)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from datetime import datetime

class PregnancyEditor(QWidget):
    """Віджет для редагування інформації про вагітність"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_controller = DataController()
        self.setup_ui()
        self.load_pregnancy_data()
    
    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Заголовок
        title = QLabel("Інформація про вагітність")
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF8C00;")
        main_layout.addWidget(title)
        
        # Скроллована область для форми
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        form_widget = QWidget()
        form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.form_layout = QFormLayout(form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)
        
        # Дата останньої менструації
        self.last_period_edit = QDateEdit()
        self.last_period_edit.setMinimumHeight(40)
        self.last_period_edit.setDisplayFormat("dd.MM.yyyy")
        self.last_period_edit.setCalendarPopup(True)
        self.last_period_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Дата останньої менструації:", self.last_period_edit)
        
        # Очікувана дата пологів
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setMinimumHeight(40)
        self.due_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Очікувана дата пологів:", self.due_date_edit)
        
        # Дата зачаття
        self.conception_edit = QDateEdit()
        self.conception_edit.setMinimumHeight(40)
        self.conception_edit.setDisplayFormat("dd.MM.yyyy")
        self.conception_edit.setCalendarPopup(True)
        self.conception_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Дата зачаття (якщо відома):", self.conception_edit)
        
        # Стать дитини
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Невідомо", "Хлопчик", "Дівчинка"])
        self.gender_combo.setMinimumHeight(40)
        self.gender_combo.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Стать дитини:", self.gender_combo)
        
        # Ім'я дитини
        self.name_edit = QLineEdit()
        self.name_edit.setMinimumHeight(40)
        self.name_edit.setPlaceholderText("Введіть ім'я, якщо вже обрали")
        self.name_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Ім'я дитини:", self.name_edit)
        
        # Додаємо форму до скроллованої області
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area, 1)
        
        # Інформація про поточний термін
        info_frame = QFrame()
        info_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        info_frame.setStyleSheet("""
            background-color: #222222;
            border-radius: 15px;
            padding: 10px;
        """)
        info_layout = QVBoxLayout(info_frame)
        
        self.week_label = QLabel("Поточний термін: ? тижнів")
        self.week_label.setFont(QFont('Arial', 14))
        info_layout.addWidget(self.week_label)
        
        self.days_left_label = QLabel("До пологів залишилось: ? днів")
        info_layout.addWidget(self.days_left_label)
        
        main_layout.addWidget(info_frame)
        
        # Кнопка збереження
        save_btn = QPushButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.setStyleSheet("""
            background-color: #FF8C00;
            border: none;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)
        save_btn.clicked.connect(self.save_pregnancy_data)
        main_layout.addWidget(save_btn)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    
    def load_pregnancy_data(self):
        """Завантажує дані про вагітність"""
        pregnancy = self.data_controller.pregnancy_data
        
        # Встановлюємо дату останньої менструації
        if pregnancy.last_period_date:
            qdate = QDate(pregnancy.last_period_date.year, pregnancy.last_period_date.month, pregnancy.last_period_date.day)
            self.last_period_edit.setDate(qdate)
        else:
            # За замовчуванням 40 тижнів тому
            self.last_period_edit.setDate(QDate.currentDate().addDays(-280))
        
        # Встановлюємо очікувану дату пологів
        if pregnancy.due_date:
            qdate = QDate(pregnancy.due_date.year, pregnancy.due_date.month, pregnancy.due_date.day)
            self.due_date_edit.setDate(qdate)
        else:
            # За замовчуванням через 40 тижнів
            self.due_date_edit.setDate(QDate.currentDate().addDays(280 - 40*7))
        
        # Встановлюємо дату зачаття
        if pregnancy.conception_date:
            qdate = QDate(pregnancy.conception_date.year, pregnancy.conception_date.month, pregnancy.conception_date.day)
            self.conception_edit.setDate(qdate)
        else:
            # За замовчуванням 38 тижнів тому
            self.conception_edit.setDate(QDate.currentDate().addDays(-266))
        
        # Встановлюємо стать дитини
        gender_index = 0  # "Невідомо" за замовчуванням
        if pregnancy.baby_gender == "Хлопчик":
            gender_index = 1
        elif pregnancy.baby_gender == "Дівчинка":
            gender_index = 2
        self.gender_combo.setCurrentIndex(gender_index)
        
        # Встановлюємо ім'я дитини
        self.name_edit.setText(pregnancy.baby_name)
        
        # Оновлюємо інформацію про термін
        self.update_pregnancy_info()
    
    def update_pregnancy_info(self):
        """Оновлює інформацію про поточний термін вагітності"""
        current_week = self.data_controller.get_current_week()
        days_left = self.data_controller.get_days_left()
        
        if current_week:
            self.week_label.setText(f"Поточний термін: {current_week} тижнів")
        else:
            self.week_label.setText("Поточний термін: не визначено")
        
        if days_left:
            self.days_left_label.setText(f"До пологів залишилось: {days_left} днів")
        else:
            self.days_left_label.setText("До пологів: не визначено")
    
    def save_pregnancy_data(self):
        """Зберігає дані про вагітність"""
        pregnancy = self.data_controller.pregnancy_data
        
        # Отримуємо дату останньої менструації
        last_period = self.last_period_edit.date()
        pregnancy.last_period_date = datetime(last_period.year(), last_period.month(), last_period.day()).date()
        
        # Отримуємо очікувану дату пологів
        due_date = self.due_date_edit.date()
        pregnancy.due_date = datetime(due_date.year(), due_date.month(), due_date.day()).date()
        
        # Отримуємо дату зачаття
        conception = self.conception_edit.date()
        pregnancy.conception_date = datetime(conception.year(), conception.month(), conception.day()).date()
        
        # Отримуємо стать дитини
        gender_index = self.gender_combo.currentIndex()
        if gender_index == 1:
            pregnancy.baby_gender = "Хлопчик"
        elif gender_index == 2:
            pregnancy.baby_gender = "Дівчинка"
        else:
            pregnancy.baby_gender = "Невідомо"
        
        # Отримуємо ім'я дитини
        pregnancy.baby_name = self.name_edit.text()
        
        # Зберігаємо дані
        self.data_controller.save_pregnancy_data()
        
        # Оновлюємо інформацію про термін
        self.update_pregnancy_info()
        
        # Повідомлення про успішне збереження
        print("Дані про вагітність успішно оновлено")

    def showEvent(self, event):
        """Оновлення даних при показі вікна"""
        super().showEvent(event)
        # Оновлюємо дані при кожному показі віджета
        self.data_controller = DataController()  # Створюємо новий контролер для отримання свіжих даних
        self.load_pregnancy_data()