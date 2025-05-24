from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QSplitter
from PyQt6.QtCore import Qt, QDate
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledDoubleSpinBox,
                               StyledButton, StyledListWidget, TitleLabel)
from styles.tools import WeightMonitorStyles
from styles.base import BaseStyles

logger = get_logger('weight_monitor')


class WeightMonitorScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()
        self.load_weight_records()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title = TitleLabel("Моніторинг ваги", 22)
        title.setStyleSheet("color: #757575; font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)

        form_frame = StyledCard("Додати новий запис")
        form_frame.setStyleSheet(WeightMonitorStyles.monitor_card())

        date_layout = QHBoxLayout()
        date_label = QLabel("Дата:")
        date_label.setStyleSheet(BaseStyles.text_primary())
        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_edit)
        form_frame.layout.addLayout(date_layout)

        weight_layout = QHBoxLayout()
        weight_label = QLabel("Вага (кг):")
        weight_label.setStyleSheet(BaseStyles.text_primary())
        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.weight_spin.setValue(60.0)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_spin)
        form_frame.layout.addLayout(weight_layout)

        # Додаємо перевірку на наявність user_profile
        initial_weight = 60.0  # Значення за замовчуванням
        if self.data_controller.user_profile:
            initial_weight = self.data_controller.user_profile.weight_before_pregnancy or 60.0

        initial_weight_label = QLabel(f"Вага до вагітності: {initial_weight} кг")
        initial_weight_label.setStyleSheet(BaseStyles.text_secondary())
        form_frame.layout.addWidget(initial_weight_label)

        save_btn = StyledButton("Зберегти запис")
        save_btn.setStyleSheet(WeightMonitorStyles.monitor_button())
        save_btn.clicked.connect(self.save_weight)
        form_frame.layout.addWidget(save_btn)

        left_layout.addWidget(form_frame)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)

        list_frame = StyledCard("Історія ваги")
        list_frame.setStyleSheet(WeightMonitorStyles.monitor_card())

        # Важливо: правильно створюємо та ініціалізуємо атрибут weight_list
        self.weight_list = StyledListWidget()
        list_frame.layout.addWidget(self.weight_list)

        refresh_btn = StyledButton("Оновити список", "secondary")
        refresh_btn.clicked.connect(self.load_weight_records)
        list_frame.layout.addWidget(refresh_btn)

        right_layout.addWidget(list_frame)
        splitter.addWidget(right_widget)

        main_layout.addWidget(splitter)

    def load_weight_records(self):
        try:
            records = self.data_controller.db.get_weight_records()

            # Перевірка, чи існує атрибут weight_list
            if not hasattr(self, 'weight_list'):
                logger.warning("Атрибут weight_list не ініціалізований")
                return

            self.weight_list.clear()

            for date, weight in records:
                item_text = f"{date}: {weight} кг"
                self.weight_list.addItem(item_text)

            logger.info(f"Завантажено {len(records)} записів ваги")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити записи ваги: {str(e)}")
            logger.error(f"Помилка при завантаженні записів ваги: {str(e)}")

    def save_weight(self):
        try:
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            weight = self.weight_spin.value()

            self.data_controller.db.add_weight_record(date_str, weight)

            # Перевірка, чи існує атрибут weight_list
            if hasattr(self, 'weight_list'):
                self.load_weight_records()

            QMessageBox.information(self, "Успіх", "Запис успішно збережено")
            logger.info(f"Збережено новий запис ваги: {date_str}, {weight} кг")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису ваги: {str(e)}")