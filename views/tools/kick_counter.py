from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QDateEdit, QTimeEdit, QSpinBox, QHBoxLayout, QListWidget,
                            QMessageBox, QSplitter, QFrame)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('kick_counter')


class KickCounterScreen(QWidget):
    """Екран для підрахунку поштовхів дитини"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_kicks()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Лічильник поштовхів")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #4CAF50;")
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

        form_title = QLabel("Записати поштовхи")
        form_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        form_title.setStyleSheet("color: #4CAF50;")
        form_layout.addWidget(form_title)

        # Інформація
        info_text = """
        <p>Підрахунок поштовхів дитини допомагає відстежувати її активність і здоров'я.</p>
        <p>Рекомендується рахувати поштовхи щодня в один і той самий час, наприклад, після їжі, 
        коли дитина найбільш активна.</p>
        <p>Занепокоєння може викликати значне зменшення кількості поштовхів.</p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #AAAAAA;")
        form_layout.addWidget(info_label)

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

        # Час
        time_layout = QHBoxLayout()
        time_label = QLabel("Час:")
        time_label.setStyleSheet("color: white;")
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setStyleSheet("""
            QTimeEdit {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_edit)
        form_layout.addLayout(time_layout)

        # Кількість поштовхів
        kicks_layout = QHBoxLayout()
        kicks_label = QLabel("Кількість поштовхів:")
        kicks_label.setStyleSheet("color: white;")
        self.kicks_spin = QSpinBox()
        self.kicks_spin.setRange(1, 100)
        self.kicks_spin.setValue(10)
        self.kicks_spin.setStyleSheet("""
            QSpinBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        kicks_layout.addWidget(kicks_label)
        kicks_layout.addWidget(self.kicks_spin)
        form_layout.addLayout(kicks_layout)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти запис")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        save_btn.clicked.connect(self.save_kicks)
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

        list_title = QLabel("Історія поштовхів")
        list_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        list_title.setStyleSheet("color: #4CAF50;")
        list_layout.addWidget(list_title)

        # Список записів
        self.kicks_list = QListWidget()
        self.kicks_list.setStyleSheet("""
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
                background-color: #4CAF50;
            }
        """)
        list_layout.addWidget(self.kicks_list)

        # Кнопка оновлення
        refresh_btn = QPushButton("Оновити історію")
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
        refresh_btn.clicked.connect(self.load_kicks)
        list_layout.addWidget(refresh_btn)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_kicks(self):
        """Завантажує історію поштовхів з бази даних"""
        try:
            kicks = self.data_controller.db.get_baby_kicks()

            self.kicks_list.clear()

            for kick in kicks:
                item_text = f"{kick['date']} {kick['time']}: {kick['count']} поштовхів"
                self.kicks_list.addItem(item_text)

            logger.info(f"Завантажено {len(kicks)} записів поштовхів")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити історію поштовхів: {str(e)}")
            logger.error(f"Помилка при завантаженні поштовхів: {str(e)}")

    def save_kicks(self):
        """Зберігає новий запис поштовхів"""
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            time_str = self.time_edit.time().toString("HH:mm")
            count = self.kicks_spin.value()

            # Зберігаємо запис у базу
            self.data_controller.db.add_baby_kick(date_str, time_str, count)

            # Оновлюємо список
            self.load_kicks()

            QMessageBox.information(self, "Успіх", "Запис поштовхів успішно збережено")
            logger.info(f"Збережено новий запис поштовхів: {date_str} {time_str}, кількість: {count}")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису поштовхів: {str(e)}")