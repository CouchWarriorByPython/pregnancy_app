from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QDateEdit, QRadioButton, QPushButton,
                             QButtonGroup, QSpacerItem, QSizePolicy, QFormLayout)
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger

logger = get_logger('pregnancy_info_screen')

class PregnancyInfoScreen(QWidget):
    """Екран для введення початкової інформації про вагітність"""

    proceed_signal = pyqtSignal(dict)  # Сигнал для переходу далі з даними

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Заголовок
        title = QLabel("Інформація про вагітність")
        title.setStyleSheet("color: #FF8C00; font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # Вертикальний спейсер для вирівнювання по центру
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))

        # Форма для введення даних
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Дата останньої менструації
        last_period_label = QLabel("Дата останньої менструації:")
        self.last_period_edit = QDateEdit()
        self.last_period_edit.setDisplayFormat("dd.MM.yyyy")
        self.last_period_edit.setCalendarPopup(True)
        self.last_period_edit.setDate(QDate.currentDate().addDays(-30))  # За замовчуванням 30 днів тому
        self.last_period_edit.setStyleSheet("""
            QDateEdit {
                background-color: #222222;
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: white;
            }
        """)
        form_layout.addRow(last_period_label, self.last_period_edit)

        # Дата зачаття (якщо відома)
        conception_label = QLabel("Дата зачаття (якщо відома):")
        self.conception_edit = QDateEdit()
        self.conception_edit.setDisplayFormat("dd.MM.yyyy")
        self.conception_edit.setCalendarPopup(True)
        self.conception_edit.setDate(QDate.currentDate().addDays(-14))  # За замовчуванням 14 днів тому
        self.conception_edit.setStyleSheet("""
            QDateEdit {
                background-color: #222222;
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: white;
            }
        """)
        form_layout.addRow(conception_label, self.conception_edit)

        main_layout.addLayout(form_layout)

        # Вертикальний спейсер
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))

        # Кнопка "Далі"
        next_btn = QPushButton("Продовжити")
        next_btn.setMinimumHeight(50)
        next_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF8C00;
                border: none;
                border-radius: 25px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
        """)
        next_btn.clicked.connect(self.on_next_clicked)
        main_layout.addWidget(next_btn)

    def on_next_clicked(self):
        """Обробка натискання кнопки Продовжити"""
        # Збираємо дані
        pregnancy_data = {
            "last_period_date": self.last_period_edit.date().toString("yyyy-MM-dd"),
            "conception_date": self.conception_edit.date().toString("yyyy-MM-dd")
        }

        logger.info(f"Дані про вагітність зібрані: {pregnancy_data}")

        # Відправляємо сигнал з даними
        self.proceed_signal.emit(pregnancy_data)