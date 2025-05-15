from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QDateEdit, QDoubleSpinBox, QHBoxLayout, QListWidget,
                             QMessageBox, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('weight_monitor')


class WeightMonitorScreen(QWidget):
    """Екран для моніторингу ваги"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_weight_records()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Моніторинг ваги")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #757575;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Додаємо спліттер для розділення форми додавання і списку записів
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # === Ліва частина - форма для додавання записів ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #222222; border-radius: 10px; padding: 10px;")
        form_layout = QVBoxLayout(form_frame)

        form_title = QLabel("Додати новий запис")
        form_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #757575;")
        form_layout.addWidget(form_title)

        # Дата
        date_layout = QHBoxLayout()
        date_label = QLabel("Дата:")
        date_label.setStyleSheet("color: white;")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        form_layout.addLayout(date_layout)

        # Вага
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Вага (кг):")
        weight_label.setStyleSheet("color: white;")
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(30.0, 150.0)
        self.weight_spin.setDecimals(1)
        self.weight_spin.setValue(60.0)
        self.weight_spin.setSingleStep(0.1)
        self.weight_spin.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_spin)
        form_layout.addLayout(weight_layout)

        # Інформація про початкову вагу
        initial_weight = self.data_controller.user_profile.weight_before_pregnancy
        initial_weight_label = QLabel(f"Вага до вагітності: {initial_weight} кг")
        initial_weight_label.setStyleSheet("color: #AAAAAA; font-style: italic;")
        form_layout.addWidget(initial_weight_label)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти запис")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        save_btn.clicked.connect(self.save_weight)
        form_layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        # === Права частина - список записів ===
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = QFrame()
        list_frame.setStyleSheet("background-color: #222222; border-radius: 10px; padding: 10px;")
        list_layout = QVBoxLayout(list_frame)

        list_title = QLabel("Історія ваги")
        list_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        list_title.setStyleSheet("color: #757575;")
        list_layout.addWidget(list_title)

        # Список записів
        self.weight_list = QListWidget()
        self.weight_list.setStyleSheet("""
            QListWidget {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #444444;
            }
            QListWidget::item:selected {
                background-color: #757575;
            }
        """)
        list_layout.addWidget(self.weight_list)

        # Кнопка оновлення
        refresh_btn = QPushButton("Оновити список")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        refresh_btn.clicked.connect(self.load_weight_records)
        list_layout.addWidget(refresh_btn)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_weight_records(self):
        """Завантажує всі записи ваги з бази даних"""
        try:
            records = self.data_controller.db.get_weight_records()

            self.weight_list.clear()

            for date, weight in records:
                item_text = f"{date}: {weight} кг"
                self.weight_list.addItem(item_text)

            logger.info(f"Завантажено {len(records)} записів ваги")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити записи ваги: {str(e)}")
            logger.error(f"Помилка при завантаженні записів ваги: {str(e)}")

    def save_weight(self):
        """Зберігає новий запис ваги"""
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            weight = self.weight_spin.value()

            # Зберігаємо запис у базу
            self.data_controller.db.add_weight_record(date_str, weight)

            # Оновлюємо список записів
            self.load_weight_records()

            QMessageBox.information(self, "Успіх", "Запис успішно збережено")
            logger.info(f"Збережено новий запис ваги: {date_str}, {weight} кг")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису ваги: {str(e)}")