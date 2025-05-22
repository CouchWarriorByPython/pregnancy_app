from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QLineEdit, QDateEdit, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QFrame,
                             QScrollArea, QFormLayout, QSizePolicy)
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from datetime import datetime
from utils.logger import get_logger

logger = get_logger('profile_editor')


class ProfileEditor(QWidget):
    """Віджет для редагування профілю користувача"""

    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Ініціалізація редактора профілю")
        self.data_controller = DataController()
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        logger.debug("Налаштування інтерфейсу редактора профілю")
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Ваш профіль")
        title.setProperty("heading", True)
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

        # Ім'я
        self.name_edit = QLineEdit()
        self.name_edit.setObjectName("name_edit")
        self.name_edit.setMinimumHeight(40)
        self.name_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Ваше ім'я:", self.name_edit)

        # Дата народження
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setObjectName("birth_date_edit")
        self.birth_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.birth_date_edit.setMinimumHeight(40)
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #222222;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                color: white;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 25px;
                border-left-width: 0px;
            }
            QDateEdit::down-arrow {
                image: url(resources/images/icons/calendar.png);
                width: 16px;
                height: 16px;
            }
        """)
        self.form_layout.addRow("Дата народження:", self.birth_date_edit)

        # Вага до вагітності
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setObjectName("weight_spin")
        self.weight_spin.setMinimumHeight(40)
        self.weight_spin.setRange(30.0, 150.0)
        self.weight_spin.setDecimals(1)
        self.weight_spin.setSuffix(" кг")
        self.weight_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Вага до вагітності:", self.weight_spin)

        # Зріст
        self.height_spin = QSpinBox()
        self.height_spin.setObjectName("height_spin")
        self.height_spin.setMinimumHeight(40)
        self.height_spin.setRange(100, 220)
        self.height_spin.setSuffix(" см")
        self.height_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Зріст:", self.height_spin)

        # Кількість попередніх вагітностей
        self.prev_pregnancies_spin = QSpinBox()
        self.prev_pregnancies_spin.setObjectName("prev_pregnancies_spin")
        self.prev_pregnancies_spin.setMinimumHeight(40)
        self.prev_pregnancies_spin.setRange(0, 10)
        self.prev_pregnancies_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Кількість попередніх вагітностей:", self.prev_pregnancies_spin)

        # Тривалість циклу
        self.cycle_spin = QSpinBox()
        self.cycle_spin.setObjectName("cycle_spin")
        self.cycle_spin.setMinimumHeight(40)
        self.cycle_spin.setRange(21, 35)
        self.cycle_spin.setSuffix(" днів")
        self.cycle_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        self.form_layout.addRow("Середня тривалість циклу:", self.cycle_spin)

        # Дієтичні вподобання (чекбокси)
        diet_frame = QFrame()
        diet_layout = QVBoxLayout(diet_frame)
        diet_layout.setContentsMargins(0, 0, 0, 0)
        diet_layout.setSpacing(5)

        self.diet_checkboxes = {}
        diet_options = ["Вегетаріанство", "Веганство", "Безглютенова дієта", "Низьколактозна дієта"]

        for option in diet_options:
            checkbox = QCheckBox(option)
            checkbox.setObjectName(f"diet_{option.lower().replace(' ', '_')}")
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 4px;
                    border: 2px solid #444444;
                }
                QCheckBox::indicator:checked {
                    background-color: #4CAF50;
                    border: 2px solid #4CAF50;
                }
            """)
            self.diet_checkboxes[option] = checkbox
            diet_layout.addWidget(checkbox)

        self.form_layout.addRow("Дієтичні вподобання:", diet_frame)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти зміни")
        save_btn.setObjectName("save_profile_btn")
        save_btn.setMinimumHeight(50)
        save_btn.setStyleSheet("""
            background-color: #FF8C00;
            border: none;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)
        save_btn.clicked.connect(self.save_profile)

        # Додаємо форму до скроллованої області
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area, 1)
        main_layout.addWidget(save_btn)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        logger.debug("Інтерфейс редактора профілю налаштовано")

    def showEvent(self, event):
        """Оновлення даних при показі вікна"""
        super().showEvent(event)
        # Оновлюємо дані при кожному показі віджета
        self.data_controller = DataController()  # Створюємо новий контролер для отримання свіжих даних
        self.load_profile_data()

    def load_profile_data(self):
        logger.info("Завантаження даних профілю")
        """Завантажує дані профілю користувача"""
        profile = self.data_controller.user_profile

        self.name_edit.setText(profile.name)
        logger.debug(f"Встановлено ім'я: {profile.name}")

        if profile.birth_date:
            qdate = QDate(profile.birth_date.year, profile.birth_date.month, profile.birth_date.day)
            self.birth_date_edit.setDate(qdate)
            logger.debug(f"Встановлено дату народження: {profile.birth_date}")
        else:
            self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))  # За замовчуванням 25 років

        self.weight_spin.setValue(profile.weight_before_pregnancy)
        logger.debug(f"Встановлено вагу до вагітності: {profile.weight_before_pregnancy} кг")
        self.height_spin.setValue(profile.height)
        logger.debug(f"Встановлено зріст: {profile.height} см")
        self.prev_pregnancies_spin.setValue(profile.previous_pregnancies)
        logger.debug(f"Встановлено кількість попередніх вагітностей: {profile.previous_pregnancies}")
        self.cycle_spin.setValue(profile.cycle_length)
        logger.debug(f"Встановлено тривалість циклу: {profile.cycle_length} днів")

        # Заповнення чекбоксів дієтичних вподобань
        for option, checkbox in self.diet_checkboxes.items():
            checkbox.setChecked(option in profile.diet_preferences)

        logger.info(f"Дані профілю користувача {profile.name} завантажено")

    def save_profile(self):
        logger.info("Зберігання змін у профілі")
        """Зберігає дані профілю користувача"""
        profile = self.data_controller.user_profile

        profile.name = self.name_edit.text()
        logger.debug(f"Встановлено ім'я: {profile.name}")

        birth_date = self.birth_date_edit.date()
        profile.birth_date = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()
        logger.debug(f"Встановлено дату народження: {profile.birth_date}")

        profile.weight_before_pregnancy = self.weight_spin.value()
        logger.debug(f"Встановлено вагу до вагітності: {profile.weight_before_pregnancy} кг")

        profile.height = self.height_spin.value()
        logger.debug(f"Встановлено зріст: {profile.height} см")

        profile.previous_pregnancies = self.prev_pregnancies_spin.value()
        logger.debug(f"Встановлено кількість попередніх вагітностей: {profile.previous_pregnancies}")

        profile.cycle_length = self.cycle_spin.value()
        logger.debug(f"Встановлено тривалість циклу: {profile.cycle_length} днів")

        # Збереження дієтичних вподобань
        profile.diet_preferences = [option for option, checkbox in self.diet_checkboxes.items() if checkbox.isChecked()]
        logger.debug(
            f"Встановлено дієтичні вподобання: {', '.join(profile.diet_preferences) if profile.diet_preferences else 'не вказано'}")

        # Зберігаємо зміни
        self.data_controller.save_user_profile()

        logger.info("Профіль успішно оновлено")