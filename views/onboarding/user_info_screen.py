from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QCheckBox, QPushButton,
                             QSpacerItem, QSizePolicy, QDateEdit,
                             QDoubleSpinBox, QSpinBox, QFormLayout, QScrollArea,
                             QFrame)
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger
from datetime import datetime

logger = get_logger('user_info_screen')


class UserInfoScreen(QWidget):
    """Екран для введення інформації про користувача"""

    proceed_signal = pyqtSignal(dict)  # Сигнал для переходу далі з даними

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Ініціалізуємо атрибути
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

        # Заголовок - профіль користувача
        user_title = QLabel("Інформація про вас")
        user_title.setStyleSheet("color: #FF8C00; font-size: 18px; font-weight: bold;")
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
        diet_label = QLabel("Дієтичні вподобання:")
        diet_label.setStyleSheet("color: white;")
        form_layout.addLayout(profile_form)
        form_layout.addWidget(diet_label)

        diet_options = ["Вегетаріанство", "Веганство", "Безглютенова дієта", "Низьколактозна дієта"]

        for option in diet_options:
            box = QCheckBox(option)
            box.setStyleSheet("""
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
            self.diet_checkboxes[option] = box
            form_layout.addWidget(box)

        # Вертикальний спейсер для заповнення простору
        form_layout.addStretch(1)

        # Кнопка "Завершити"
        finish_btn = QPushButton("Завершити")
        finish_btn.setMinimumHeight(50)
        finish_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF8C00;
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        finish_btn.clicked.connect(self.on_finish_clicked)
        form_layout.addWidget(finish_btn)

        # Додаємо форму до скролованої області
        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

    def on_finish_clicked(self):
        """Обробка натискання кнопки Завершити"""
        # Збираємо дані
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

        logger.info(f"Дані користувача зібрані: {user_data}")

        # Відправляємо сигнал з даними
        self.proceed_signal.emit(user_data)