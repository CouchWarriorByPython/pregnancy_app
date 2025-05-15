from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QCheckBox, QRadioButton, QPushButton,
                             QButtonGroup, QSpacerItem, QSizePolicy, QDateEdit,
                             QDoubleSpinBox, QSpinBox, QFormLayout, QScrollArea,
                             QFrame)
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger
from datetime import datetime

logger = get_logger('child_info_screen')


class ChildInfoScreen(QWidget):
    """Екран для введення інформації про дитину та користувача"""

    proceed_signal = pyqtSignal(dict)  # Сигнал для переходу далі з даними

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Ініціалізуємо атрибути
        self.name_input = None
        self.first_labour_checkbox = None
        self.gender_group = None
        self.terms_checkbox = None

        # Профіль користувача
        self.user_name_input = None
        self.birth_date_edit = None
        self.weight_spin = None
        self.height_spin = None
        self.cycle_spin = None
        self.diet_checkboxes = {}

        self.setup_ui()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Скролована область для форми
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)

        # Заголовок - інформація про дитину
        baby_title = QLabel("Інформація про дитину")
        baby_title.setStyleSheet("color: #FF8C00; font-size: 18px; font-weight: bold;")
        form_layout.addWidget(baby_title)

        # Поле для імені дитини
        name_label = QLabel("Ім'я дитини")
        name_label.setStyleSheet("color: #AAAAAA;")
        form_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Залиште поле порожнім, якщо ви ще не обрали ім'я")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #222222;
                border: none;
                border-bottom: 1px solid #444444;
                color: white;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-bottom: 1px solid #FF8C00;
            }
        """)
        form_layout.addWidget(self.name_input)

        # Опція "Це мої перші пологи"
        self.first_labour_checkbox = QCheckBox("Це мої перші пологи")
        self.first_labour_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #444444;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }
        """)
        form_layout.addWidget(self.first_labour_checkbox)

        # Вибір статі дитини
        gender_label = QLabel("Стать дитини")
        gender_label.setStyleSheet("color: white; font-size: 16px;")
        form_layout.addWidget(gender_label)

        # Група для радіокнопок статі
        self.gender_group = QButtonGroup(self)

        # Макет для радіокнопок
        gender_layout = QVBoxLayout()
        gender_layout.setSpacing(10)

        # Радіокнопки для статі
        gender_options = [
            ("♂ Хлопчик", "Хлопчик"),
            ("♀ Дівчинка", "Дівчинка"),
            ("⚥ Ще не знаю", "Невідомо")
        ]

        for i, (text, value) in enumerate(gender_options):
            radio = QRadioButton(text)
            radio.setStyleSheet("""
                QRadioButton {
                    color: white;
                    font-size: 14px;
                }
                QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                    border-radius: 10px;
                    border: 2px solid #444444;
                }
                QRadioButton::indicator:checked {
                    background-color: #FF8C00;
                    border: 2px solid #FF8C00;
                }
            """)
            radio.gender_value = value
            self.gender_group.addButton(radio, i)
            gender_layout.addWidget(radio)

            # За замовчуванням вибираємо "Ще не знаю"
            if i == 2:
                radio.setChecked(True)

        form_layout.addLayout(gender_layout)

        # Заголовок - профіль користувача
        user_title = QLabel("Інформація про вас")
        user_title.setStyleSheet("color: #FF8C00; font-size: 18px; font-weight: bold; margin-top: 10px;")
        form_layout.addWidget(user_title)

        # Форма профілю
        profile_form = QFormLayout()
        profile_form.setSpacing(15)

        # Ваше ім'я
        self.user_name_input = QLineEdit()
        self.user_name_input.setPlaceholderText("Введіть ваше ім'я")
        self.user_name_input.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
            min-height: 30px;
        """)
        profile_form.addRow("Ваше ім'я:", self.user_name_input)

        # Дата народження
        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.birth_date_edit.setMinimumHeight(40)
        self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))  # За замовчуванням 25 років
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        profile_form.addRow("Дата народження:", self.birth_date_edit)

        # Вага до вагітності
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setMinimumHeight(40)
        self.weight_spin.setRange(30.0, 150.0)
        self.weight_spin.setDecimals(1)
        self.weight_spin.setValue(60.0)
        self.weight_spin.setSuffix(" кг")
        self.weight_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        profile_form.addRow("Вага до вагітності:", self.weight_spin)

        # Зріст
        self.height_spin = QSpinBox()
        self.height_spin.setMinimumHeight(40)
        self.height_spin.setRange(100, 220)
        self.height_spin.setValue(165)
        self.height_spin.setSuffix(" см")
        self.height_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        profile_form.addRow("Зріст:", self.height_spin)

        # Тривалість циклу
        self.cycle_spin = QSpinBox()
        self.cycle_spin.setMinimumHeight(40)
        self.cycle_spin.setRange(21, 35)
        self.cycle_spin.setValue(28)
        self.cycle_spin.setSuffix(" днів")
        self.cycle_spin.setStyleSheet("""
            background-color: #222222;
            border: none;
            border-radius: 8px;
            padding: 5px 10px;
            color: white;
        """)
        profile_form.addRow("Середня тривалість циклу:", self.cycle_spin)

        # Дієтичні вподобання (чекбокси)
        diet_frame = QFrame()
        diet_layout = QVBoxLayout(diet_frame)
        diet_layout.setContentsMargins(0, 0, 0, 0)
        diet_layout.setSpacing(5)

        self.diet_checkboxes = {}
        diet_options = ["Вегетаріанство", "Веганство", "Безглютенова дієта", "Низьколактозна дієта"]

        for option in diet_options:
            checkbox = QCheckBox(option)
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

        profile_form.addRow("Дієтичні вподобання:", diet_frame)

        form_layout.addLayout(profile_form)

        # Чекбокс з умовами
        self.terms_checkbox = QCheckBox("Я погоджуюсь з умовами користування")
        self.terms_checkbox.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                margin-top: 20px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #444444;
            }
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 2px solid #4CAF50;
            }
        """)
        form_layout.addWidget(self.terms_checkbox)

        # Кнопка "Далі"
        next_btn = QPushButton("Далі")
        next_btn.setMinimumHeight(50)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #AAAAAA;
                border: none;
                border-radius: 25px;
                color: black;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:enabled {
                background-color: #4CAF50;
                color: white;
            }
        """)
        next_btn.clicked.connect(self.on_next_clicked)
        # Кнопка неактивна, поки не погоджені умови
        next_btn.setEnabled(False)
        self.terms_checkbox.toggled.connect(lambda checked: next_btn.setEnabled(checked))

        form_layout.addWidget(next_btn)

        # Додаємо форму до скролованої області
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

    def on_next_clicked(self):
        """Обробка натискання кнопки Далі"""
        # Збираємо дані про дитину
        child_data = {
            "name": self.name_input.text().strip(),
            "first_labour": self.first_labour_checkbox.isChecked(),
            "gender": self.get_selected_gender()
        }

        # Збираємо дані профілю користувача
        birth_date = self.birth_date_edit.date()
        birth_date_str = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date().isoformat()

        # Дієтичні вподобання
        diet_preferences = [option for option, checkbox in self.diet_checkboxes.items()
                            if checkbox.isChecked()]

        user_data = {
            "name": self.user_name_input.text().strip(),
            "birth_date": birth_date_str,
            "weight_before_pregnancy": self.weight_spin.value(),
            "height": self.height_spin.value(),
            "cycle_length": self.cycle_spin.value(),
            "diet_preferences": diet_preferences
        }

        # Додаємо дані користувача до даних дитини
        child_data["user_data"] = user_data

        logger.info(f"Дані дитини зібрані: {child_data}")

        # Відправляємо сигнал з даними
        self.proceed_signal.emit(child_data)

    def get_selected_gender(self):
        """Отримує вибрану стать"""
        selected_button = self.gender_group.checkedButton()
        if selected_button:
            return selected_button.gender_value
        return "Невідомо"