from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QDateEdit, QDoubleSpinBox, QListWidget,
                             QMessageBox, QSplitter, QFrame,
                             QFormLayout, QLineEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('belly_tracker')


class BellyTrackerScreen(QWidget):
    """Екран для відстеження розміру живота"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_measurements()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Відстеження розміру живота")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF9800;")
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
        form_title.setStyleSheet("color: #FF9800;")
        form_layout.addWidget(form_title)

        # Інформація
        info_text = """
        <p>Відстеження розміру живота допомагає контролювати ріст дитини протягом вагітності.</p>
        <p>Вимірювання проводиться сантиметровою стрічкою по найбільшому обхвату живота на рівні пупка.</p>
        <p>Рекомендується проводити вимірювання раз на 2-4 тижні.</p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #AAAAAA;")
        form_layout.addWidget(info_label)

        # Форма для введення даних
        input_form = QFormLayout()

        # Дата
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
        input_form.addRow("Дата:", self.date_edit)

        # Розмір живота
        self.measurement_spin = QDoubleSpinBox()
        self.measurement_spin.setRange(50.0, 150.0)
        self.measurement_spin.setDecimals(1)
        self.measurement_spin.setValue(80.0)
        self.measurement_spin.setSuffix(" см")
        self.measurement_spin.setStyleSheet("""
                    QDoubleSpinBox {
                        background-color: #333333;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        padding: 5px;
                    }
                """)
        input_form.addRow("Розмір живота:", self.measurement_spin)

        # Нотатки
        self.notes_edit = QLineEdit()
        self.notes_edit.setPlaceholderText("Додаткові нотатки (необов'язково)")
        self.notes_edit.setStyleSheet("""
                    QLineEdit {
                        background-color: #333333;
                        border: none;
                        border-radius: 5px;
                        color: white;
                        padding: 5px;
                    }
                """)
        input_form.addRow("Нотатки:", self.notes_edit)

        form_layout.addLayout(input_form)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти запис")
        save_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FF9800;
                        color: white;
                        border-radius: 5px;
                        padding: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #F57C00;
                    }
                """)
        save_btn.clicked.connect(self.save_measurement)
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

        list_title = QLabel("Історія вимірювань")
        list_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        list_title.setStyleSheet("color: #FF9800;")
        list_layout.addWidget(list_title)

        # Список записів
        self.measurement_list = QListWidget()
        self.measurement_list.setStyleSheet("""
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
                        background-color: #FF9800;
                    }
                """)
        list_layout.addWidget(self.measurement_list)

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
        refresh_btn.clicked.connect(self.load_measurements)
        list_layout.addWidget(refresh_btn)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_measurements(self):
        """Завантажує записи про розміри живота з бази даних"""
        try:
            measurements = self.data_controller.db.get_belly_measurements()

            self.measurement_list.clear()

            for measurement in measurements:
                item_text = f"{measurement['date']}: {measurement['measurement']} см"
                if measurement['notes']:
                    item_text += f" - {measurement['notes']}"

                self.measurement_list.addItem(item_text)

            logger.info(f"Завантажено {len(measurements)} записів про розміри живота")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити вимірювання: {str(e)}")
            logger.error(f"Помилка при завантаженні вимірювань: {str(e)}")

    def save_measurement(self):
        """Зберігає новий запис про розмір живота"""
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            measurement = self.measurement_spin.value()
            notes = self.notes_edit.text().strip()

            # Зберігаємо запис у базу
            self.data_controller.db.add_belly_measurement(date_str, measurement, notes)

            # Очищаємо поля нотаток
            self.notes_edit.clear()

            # Оновлюємо список
            self.load_measurements()

            QMessageBox.information(self, "Успіх", "Запис про розмір живота успішно збережено")
            logger.info(f"Збережено новий запис про розмір живота: {date_str}, {measurement} см")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису про розмір живота: {str(e)}")