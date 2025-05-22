from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QSplitter, QFormLayout
from PyQt6.QtCore import Qt, QDate
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledDoubleSpinBox,
                               StyledInput, StyledButton, StyledListWidget, TitleLabel)
from utils.styles import Styles

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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Відстеження розміру живота", 22)
        title.setStyleSheet("color: #FF9800;")
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # === Ліва частина - форма для додавання записів ===
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Додати новий запис")
        form_frame.setStyleSheet(form_frame.styleSheet() + "QLabel { color: #FF9800; }")

        info_text = """
        <p>Відстеження розміру живота допомагає контролювати ріст дитини протягом вагітності.</p>
        <p>Вимірювання проводиться сантиметровою стрічкою по найбільшому обхвату живота на рівні пупка.</p>
        <p>Рекомендується проводити вимірювання раз на 2-4 тижні.</p>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setStyleSheet(Styles.text_secondary())
        form_frame.layout.addWidget(info_label)

        input_form = QFormLayout()

        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        input_form.addRow("Дата:", self.date_edit)

        self.measurement_spin = StyledDoubleSpinBox(50.0, 150.0, 1, " см")
        self.measurement_spin.setValue(80.0)
        input_form.addRow("Розмір живота:", self.measurement_spin)

        self.notes_edit = StyledInput("Додаткові нотатки (необов'язково)")
        input_form.addRow("Нотатки:", self.notes_edit)

        form_frame.layout.addLayout(input_form)

        save_btn = StyledButton("Зберегти запис")
        save_btn.setStyleSheet("background-color: #FF9800; QPushButton:hover { background-color: #F57C00; }")
        save_btn.clicked.connect(self.save_measurement)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        # === Права частина - список записів ===
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Історія вимірювань")
        list_frame.setStyleSheet(list_frame.styleSheet() + "QLabel { color: #FF9800; }")

        self.measurement_list = StyledListWidget()
        list_frame.layout.addWidget(self.measurement_list)

        refresh_btn = StyledButton("Оновити список", "secondary")
        refresh_btn.clicked.connect(self.load_measurements)
        list_frame.layout.addWidget(refresh_btn)

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

            self.data_controller.db.add_belly_measurement(date_str, measurement, notes)
            self.notes_edit.clear()
            self.load_measurements()

            QMessageBox.information(self, "Успіх", "Запис про розмір живота успішно збережено")
            logger.info(f"Збережено новий запис про розмір живота: {date_str}, {measurement} см")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису про розмір живота: {str(e)}")