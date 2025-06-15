from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox, QSplitter, QFormLayout, QAbstractSpinBox
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import Qt, QDate
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledDoubleSpinBox,
                                StyledInput, StyledButton, StyledListWidget, TitleLabel)
from styles import BellyTrackerStyles, BaseStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('belly_tracker')


class BellyTrackerScreen(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(12)

        # Простий заголовок
        title = TitleLabel("Відстеження розміру живота", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Контролюйте ріст дитини протягом вагітності")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Інформація без фону
        info_title = QLabel("📏 Про вимірювання живота")
        info_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(info_title)

        info_text = """• Вимірювання допомагає контролювати ріст дитини
• Проводиться сантиметровою стрічкою по найбільшому обхвату
• Вимірюйте на рівні пупка
• Рекомендується робити раз на 2-4 тижні"""

        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; background: transparent; border: none;")
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)

        # Відступ
        main_layout.addSpacing(20)

        # Форма з підкресленими полями
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        form_layout.setHorizontalSpacing(20)

        # Дата
        date_label = QLabel("📅 Дата:")
        date_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        date_label.setMinimumHeight(24)

        self.date_edit = StyledDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        form_layout.addRow(date_label, self.date_edit)

        # Розмір живота
        measurement_label = QLabel("📏 Розмір живота:")
        measurement_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        measurement_label.setMinimumHeight(24)

        self.measurement_spin = StyledDoubleSpinBox(60.0, 160.0, 1, " см")
        self.measurement_spin.setValue(80.0)
        self.measurement_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.measurement_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.measurement_spin.setMinimumHeight(24)
        self.measurement_spin.setMaximumHeight(40)

        form_layout.addRow(measurement_label, self.measurement_spin)

        # Нотатки
        notes_label = QLabel("📝 Нотатки:")
        notes_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        notes_label.setMinimumHeight(24)

        self.notes_edit = StyledInput("Додаткові нотатки (необов'язково)")
        self.notes_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.notes_edit.setMinimumHeight(24)
        self.notes_edit.setMaximumHeight(40)

        form_layout.addRow(notes_label, self.notes_edit)

        main_layout.addLayout(form_layout)

        # Відступ
        main_layout.addSpacing(20)

        # Кнопка збереження
        save_btn = StyledButton("💾 Зберегти запис")
        save_btn.setMinimumHeight(44)
        save_btn.setStyleSheet(BellyTrackerStyles.tracker_button())
        save_btn.clicked.connect(self.save_measurement)
        main_layout.addWidget(save_btn)

        # Відступ
        main_layout.addSpacing(20)

        # Історія без рамки
        history_title = QLabel("📊 Історія вимірювань")
        history_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(history_title)

        self.measurement_list = StyledListWidget()
        self.measurement_list.setStyleSheet("""
            QListWidget {
                background: transparent; 
                border: none; 
                border-bottom: 2px solid rgba(255, 255, 255, 0.3); 
                color: white; 
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px 4px;
                border: none;
                background: transparent;
                color: white;
                min-height: 20px;
            }
            QListWidget::item:selected {
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }
        """)
        self.measurement_list.setWordWrap(True)
        self.measurement_list.setTextElideMode(Qt.TextElideMode.ElideNone)
        main_layout.addWidget(self.measurement_list)

        # Розтягуючий spacer
        main_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self.load_measurements()

    def load_measurements(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для перегляду записів")
            return

        try:
            user_id = self.get_current_user_id()
            measurements = self.data_controller.db.get_belly_measurements(user_id)
            self.measurement_list.clear()

            for measurement in measurements:
                item_text = f"{measurement['date']}: {measurement['measurement']} см"
                if measurement['notes']:
                    item_text += f" - {measurement['notes']}"
                self.measurement_list.addItem(item_text)

            logger.info(f"Завантажено {len(measurements)} записів про розміри живота для користувача {user_id}")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося завантажити вимірювання: {str(e)}")
            logger.error(f"Помилка при завантаженні вимірювань для користувача {user_id}: {str(e)}")

    def save_measurement(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження записів")
            return

        try:
            user_id = self.get_current_user_id()
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            measurement = self.measurement_spin.value()
            notes = self.notes_edit.text().strip()

            if measurement < 60.0 or measurement > 160.0:
                show_warning(self, "Помилка", "Введіть реальний розмір живота")
                return

            self.data_controller.db.add_belly_measurement(date_str, measurement, notes, user_id)
            self.notes_edit.clear()
            self.load_measurements()

            show_info(self, "Успіх", "Запис збережено")
            logger.info(
                f"Збережено новий запис про розмір живота для користувача {user_id}: {date_str}, {measurement} см")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису про розмір живота для користувача {user_id}: {str(e)}")