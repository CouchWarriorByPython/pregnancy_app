from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QCheckBox, QRadioButton, QPushButton,
                             QButtonGroup, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import pyqtSignal
from utils.logger import get_logger

logger = get_logger('child_info_screen')


class ChildInfoScreen(QWidget):
    """Екран для введення інформації про дитину"""

    proceed_signal = pyqtSignal(dict)  # Сигнал для переходу далі з даними

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Ініціалізуємо атрибути
        self.name_input = None
        self.first_labour_checkbox = None
        self.gender_group = None
        self.terms_checkbox = None

        self.setup_ui()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Вертикальний спейсер для вирівнювання по центру
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))

        # Поле для імені дитини
        name_label = QLabel("Ім'я дитини")
        name_label.setStyleSheet("color: #AAAAAA;")
        main_layout.addWidget(name_label)

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
        main_layout.addWidget(self.name_input)

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
        main_layout.addWidget(self.first_labour_checkbox)

        # Спейсер
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Fixed))

        # Вибір статі дитини
        gender_label = QLabel("Стать дитини")
        gender_label.setStyleSheet("color: white; font-size: 16px;")
        main_layout.addWidget(gender_label)

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

        main_layout.addLayout(gender_layout)

        # Спейсер
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))

        # Чекбокс з умовами
        self.terms_checkbox = QCheckBox("Я погоджуюсь з умовами користування")
        self.terms_checkbox.setStyleSheet("""
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
        main_layout.addWidget(self.terms_checkbox)

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

        main_layout.addWidget(next_btn)

    def on_next_clicked(self):
        """Обробка натискання кнопки Далі"""
        # Збираємо дані
        child_data = {
            "name": self.name_input.text().strip(),
            "first_labour": self.first_labour_checkbox.isChecked(),
            "gender": self.get_selected_gender()
        }

        logger.info(f"Дані дитини зібрані: {child_data}")

        # Відправляємо сигнал з даними
        self.proceed_signal.emit(child_data)

    def get_selected_gender(self):
        """Отримує вибрану стать"""
        selected_button = self.gender_group.checkedButton()
        if selected_button:
            return selected_button.gender_value
        return "Невідомо"