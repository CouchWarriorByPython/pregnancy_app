from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QSplitter, QFormLayout, QAbstractSpinBox
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import Qt, QDate, QTime
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledTimeEdit, StyledSpinBox,
                                StyledButton, StyledListWidget, TitleLabel, StyledInput)
from styles import KickCounterStyles, BaseStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('kick_counter')


class KickCounterScreen(QWidget, UserMixin):
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
        title = TitleLabel("Лічильник поштовхів", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Відстежуйте активність вашої дитини")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Інформація без фону
        info_title = QLabel("👶 Про підрахунок поштовхів")
        info_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(info_title)

        info_text = """• Підрахунок поштовхів допомагає відстежувати здоров'я дитини
• Рекомендується рахувати щодня в один і той самий час
• Найкраще після їжі, коли дитина найбільш активна
• Зменшення активності може бути сигналом для консультації з лікарем"""

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

        self.date_edit = StyledInput("дд.мм.рррр")
        self.date_edit.setText(QDate.currentDate().toString("dd.MM.yyyy"))
        self.date_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.date_edit.setMinimumHeight(24)
        self.date_edit.setMaximumHeight(40)
        form_layout.addRow(date_label, self.date_edit)

        # Час
        time_label = QLabel("🕐 Час:")
        time_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        time_label.setMinimumHeight(24)

        self.time_edit = StyledInput("гг:хх")
        self.time_edit.setText(QTime.currentTime().toString("HH:mm"))
        self.time_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.time_edit.setMinimumHeight(24)
        self.time_edit.setMaximumHeight(40)

        form_layout.addRow(time_label, self.time_edit)

        # Кількість поштовхів
        kicks_label = QLabel("👶 Кількість поштовхів:")
        kicks_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        kicks_label.setMinimumHeight(24)

        self.kicks_spin = StyledSpinBox(1, 100)
        self.kicks_spin.setValue(10)
        self.kicks_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.kicks_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.kicks_spin.setMinimumHeight(24)
        self.kicks_spin.setMaximumHeight(40)

        form_layout.addRow(kicks_label, self.kicks_spin)

        main_layout.addLayout(form_layout)

        # Відступ
        main_layout.addSpacing(20)

        # Кнопка збереження
        save_btn = StyledButton("💾 Зберегти запис")
        save_btn.setMinimumHeight(44)
        save_btn.setStyleSheet(KickCounterStyles.counter_button())
        save_btn.clicked.connect(self.save_kicks)
        main_layout.addWidget(save_btn)

        # Відступ
        main_layout.addSpacing(20)

        # Історія без рамки
        history_title = QLabel("📊 Історія поштовхів")
        history_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(history_title)

        self.kicks_list = StyledListWidget()
        self.kicks_list.setStyleSheet("""
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
        self.kicks_list.setWordWrap(True)
        self.kicks_list.setTextElideMode(Qt.TextElideMode.ElideNone)
        main_layout.addWidget(self.kicks_list)

        # Розтягуючий spacer
        main_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self.load_kicks()

    def load_kicks(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для перегляду записів")
            return

        try:
            user_id = self.get_current_user_id()
            kicks = self.data_controller.db.get_baby_kicks(user_id)
            self.kicks_list.clear()

            for kick in kicks:
                item_text = f"{kick['date']} {kick['time']}: {kick['count']} поштовхів"
                self.kicks_list.addItem(item_text)

            logger.info(f"Завантажено {len(kicks)} записів поштовхів для користувача {user_id}")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося завантажити історію поштовхів: {str(e)}")
            logger.error(f"Помилка при завантаженні поштовхів для користувача {user_id}: {str(e)}")

    def save_kicks(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження записів")
            return

        try:
            user_id = self.get_current_user_id()
            date_text = self.date_edit.text().strip()
            time_text = self.time_edit.text().strip()
            
            # Валідація дати
            try:
                date_parts = date_text.split('.')
                if len(date_parts) != 3:
                    show_warning(self, "Помилка", "Невірний формат дати. Використовуйте формат дд.мм.рррр")
                    return
                    
                day, month, year = map(int, date_parts)
                qdate = QDate(year, month, day)
                if not qdate.isValid():
                    show_warning(self, "Помилка", "Невірна дата")
                    return
                date_str = qdate.toString("yyyy-MM-dd")
            except ValueError:
                show_warning(self, "Помилка", "Невірний формат дати. Використовуйте формат дд.мм.рррр")
                return
                
            # Валідація часу
            try:
                time_parts = time_text.split(':')
                if len(time_parts) != 2:
                    show_warning(self, "Помилка", "Невірний формат часу. Використовуйте формат гг:хх")
                    return
                    
                hour, minute = map(int, time_parts)
                if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                    show_warning(self, "Помилка", "Невірний час. Години: 0-23, хвилини: 0-59")
                    return
                time_str = f"{hour:02d}:{minute:02d}"
            except ValueError:
                show_warning(self, "Помилка", "Невірний формат часу. Використовуйте формат гг:хх")
                return
                
            count = self.kicks_spin.value()

            if count < 1:
                show_warning(self, "Помилка", "Кількість поштовхів повинна бути більше 0")
                return

            self.data_controller.db.add_baby_kick(date_str, time_str, count, user_id)
            self.load_kicks()

            show_info(self, "Успіх", "Запис поштовхів успішно збережено")
            logger.info(
                f"Збережено новий запис поштовхів для користувача {user_id}: {date_str} {time_str}, кількість: {count}")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису поштовхів для користувача {user_id}: {str(e)}")