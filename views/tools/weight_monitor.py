from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QSplitter, QFormLayout, QAbstractSpinBox
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import Qt, QDate
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledDoubleSpinBox,
                                StyledButton, StyledListWidget, TitleLabel, StyledInput)
from styles import WeightMonitorStyles, BaseStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('weight_monitor')


class WeightMonitorScreen(QWidget, UserMixin):
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
        title = TitleLabel("Моніторинг ваги", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Відстежуйте зміни ваги під час вагітності")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Форма з підкресленими полями
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        form_layout.setHorizontalSpacing(20)

        # Дата
        date_label = QLabel("📅 Дата:")
        date_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        date_label.setMinimumHeight(24)

        self.date_edit = StyledInput("дд.мм.рррр")
        self.date_edit.setText(QDate.currentDate().toString("dd.MM.yyyy"))
        self.date_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.date_edit.setMinimumHeight(24)
        self.date_edit.setMaximumHeight(40)
        form_layout.addRow(date_label, self.date_edit)

        # Вага
        weight_label = QLabel("⚖️ Вага:")
        weight_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        weight_label.setMinimumHeight(24)

        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.weight_spin.setValue(60.0)
        self.weight_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.weight_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.weight_spin.setMinimumHeight(24)
        self.weight_spin.setMaximumHeight(40)

        form_layout.addRow(weight_label, self.weight_spin)

        main_layout.addLayout(form_layout)

        # Інформація про початкову вагу
        self.initial_weight_label = QLabel("📊 Вага до вагітності: не визначено")
        self.initial_weight_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(self.initial_weight_label)

        # Відступ
        main_layout.addSpacing(20)

        # Кнопка збереження
        save_btn = StyledButton("💾 Зберегти запис")
        save_btn.setMinimumHeight(44)
        save_btn.setStyleSheet(WeightMonitorStyles.monitor_button())
        save_btn.clicked.connect(self.save_weight)
        main_layout.addWidget(save_btn)

        # Розтягуючий spacer для опускання історії
        main_layout.addStretch()

        # Історія без рамки
        history_title = QLabel("📈 Історія ваги")
        history_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(history_title)

        self.weight_list = StyledListWidget()
        self.weight_list.setStyleSheet("""
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
        self.weight_list.setWordWrap(True)
        self.weight_list.setTextElideMode(Qt.TextElideMode.ElideNone)
        main_layout.addWidget(self.weight_list)

        # Розтягуючий spacer
        main_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self._update_initial_weight()
            self.load_weight_records()

    def _update_initial_weight(self):
        if self.data_controller and self.data_controller.user_profile:
            initial_weight = self.data_controller.user_profile.weight_before_pregnancy or 60.0
            self.initial_weight_label.setText(f"Вага до вагітності: {initial_weight} кг")

    def load_weight_records(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для перегляду записів")
            return

        try:
            user_id = self.get_current_user_id()
            records = self.data_controller.db.get_weight_records(user_id)
            self.weight_list.clear()

            for date, weight in records:
                item_text = f"{date}: {weight} кг"
                self.weight_list.addItem(item_text)

            logger.info(f"Завантажено {len(records)} записів ваги для користувача {user_id}")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося завантажити записи ваги: {str(e)}")
            logger.error(f"Помилка при завантаженні записів ваги для користувача {user_id}: {str(e)}")

    def save_weight(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження записів")
            return

        try:
            user_id = self.get_current_user_id()
            date_text = self.date_edit.text()
            
            # Парсимо дату з тексту
            try:
                date_parts = date_text.split('.')
                if len(date_parts) == 3:
                    day, month, year = map(int, date_parts)
                    qdate = QDate(year, month, day)
                    date_str = qdate.toString("yyyy-MM-dd")
                else:
                    date_str = QDate.currentDate().toString("yyyy-MM-dd")
            except:
                date_str = QDate.currentDate().toString("yyyy-MM-dd")
                
            weight = self.weight_spin.value()

            if weight < 30.0 or weight > 300.0:
                show_warning(self, "Помилка", "Введіть реальне значення ваги")
                return

            self.data_controller.db.add_weight_record(date_str, weight, user_id)
            self.load_weight_records()

            show_info(self, "Успіх", "Запис успішно збережено")
            logger.info(f"Збережено новий запис ваги для користувача {user_id}: {date_str}, {weight} кг")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису ваги для користувача {user_id}: {str(e)}")