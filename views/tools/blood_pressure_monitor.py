from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QDateEdit, QTimeEdit, QSpinBox, QHBoxLayout, QListWidget,
                             QMessageBox, QSplitter, QFrame,
                             QFormLayout, QLineEdit, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('blood_pressure_monitor')


class BloodPressureMonitorScreen(QWidget):
    """Екран для моніторингу артеріального тиску"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_pressure_records()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Заголовок
        title = QLabel("Моніторинг артеріального тиску")
        title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #E91E63;")
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
        form_title.setStyleSheet("color: #E91E63;")
        form_layout.addWidget(form_title)

        # Інформація
        info_text = """
        <p>Регулярне вимірювання артеріального тиску важливе під час вагітності для раннього виявлення 
        можливих ускладнень.</p>
        <p>Нормальний тиск під час вагітності: 110-120/70-80 мм рт.ст.</p>
        <p>Підвищений тиск може бути ознакою прееклампсії і потребує консультації лікаря.</p>
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

        # Час
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
        input_form.addRow("Час:", self.time_edit)

        # Систолічний тиск (верхній)
        self.systolic_spin = QSpinBox()
        self.systolic_spin.setRange(80, 200)
        self.systolic_spin.setValue(120)
        self.systolic_spin.setStyleSheet("""
            QSpinBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        input_form.addRow("Верхній тиск:", self.systolic_spin)

        # Діастолічний тиск (нижній)
        self.diastolic_spin = QSpinBox()
        self.diastolic_spin.setRange(40, 120)
        self.diastolic_spin.setValue(80)
        self.diastolic_spin.setStyleSheet("""
            QSpinBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        input_form.addRow("Нижній тиск:", self.diastolic_spin)

        # Пульс
        self.pulse_spin = QSpinBox()
        self.pulse_spin.setRange(40, 200)
        self.pulse_spin.setValue(75)
        self.pulse_spin.setStyleSheet("""
            QSpinBox {
                background-color: #333333;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        input_form.addRow("Пульс:", self.pulse_spin)

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

        # Додаємо прогалину
        form_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Кнопка збереження
        save_btn = QPushButton("Зберегти запис")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C2185B;
            }
        """)
        save_btn.clicked.connect(self.save_pressure)
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
        list_title.setStyleSheet("color: #E91E63;")
        list_layout.addWidget(list_title)

        # Список записів
        self.pressure_list = QListWidget()
        self.pressure_list.setStyleSheet("""
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
                background-color: #E91E63;
            }
        """)
        list_layout.addWidget(self.pressure_list)

        # Кнопки для фільтрації
        buttons_layout = QHBoxLayout()

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
        refresh_btn.clicked.connect(self.load_pressure_records)

        period_label = QLabel("Показати за:")
        period_label.setStyleSheet("color: white;")

        self.period_spin = QSpinBox()
        self.period_spin.setRange(7, 90)
        self.period_spin.setValue(30)
        self.period_spin.setSuffix(" днів")
        self.period_spin.setStyleSheet("""
            QSpinBox {
                background-color: #444444;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 5px;
            }
        """)
        self.period_spin.valueChanged.connect(self.load_pressure_records)

        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addWidget(period_label)
        buttons_layout.addWidget(self.period_spin)

        list_layout.addLayout(buttons_layout)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_pressure_records(self):
        """Завантажує записи про тиск з бази даних"""
        try:
            days = self.period_spin.value() if hasattr(self, 'period_spin') else 30

            records = self.data_controller.db.get_blood_pressure(days)

            self.pressure_list.clear()

            for record in records:
                item_text = f"{record['date']} {record['time']}: {record['systolic']}/{record['diastolic']} мм рт.ст."
                if record['pulse']:
                    item_text += f", пульс: {record['pulse']}"
                if record['notes']:
                    item_text += f" - {record['notes']}"

                self.pressure_list.addItem(item_text)

            logger.info(f"Завантажено {len(records)} записів про тиск за {days} днів")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити записи про тиск: {str(e)}")
            logger.error(f"Помилка при завантаженні записів про тиск: {str(e)}")

    def save_pressure(self):
        """Зберігає новий запис про тиск"""
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            time_str = self.time_edit.time().toString("HH:mm")
            systolic = self.systolic_spin.value()
            diastolic = self.diastolic_spin.value()
            pulse = self.pulse_spin.value()
            notes = self.notes_edit.text().strip()

            # Перевірка співвідношення верхнього і нижнього тиску
            if systolic <= diastolic:
                QMessageBox.warning(self, "Попередження",
                                    "Верхній тиск повинен бути більшим за нижній.\nПеревірте правильність введених значень.")
                return

            # Зберігаємо запис у базу
            self.data_controller.db.add_blood_pressure(date_str, time_str, systolic, diastolic, pulse, notes)

            # Очищаємо поля нотаток
            self.notes_edit.clear()

            # Оновлюємо список
            self.load_pressure_records()

            QMessageBox.information(self, "Успіх", "Запис тиску успішно збережено")
            logger.info(f"Збережено новий запис тиску: {date_str} {time_str}, {systolic}/{diastolic}, пульс: {pulse}")

            # Перевірка на підвищений тиск
            if systolic >= 140 or diastolic >= 90:
                QMessageBox.warning(self, "Увага! Підвищений тиск",
                                    f"Ваш тиск {systolic}/{diastolic} мм рт.ст. перевищує норму.\n"
                                    "Рекомендується проконсультуватися з лікарем.")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису тиску: {str(e)}")