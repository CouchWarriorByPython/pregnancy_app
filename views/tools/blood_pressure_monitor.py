from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout,
                             QMessageBox, QSplitter, QFormLayout, QSpacerItem, QSizePolicy, QAbstractSpinBox)
from utils.message_utils import show_info, show_warning, show_error
from PyQt6.QtCore import Qt, QDate, QTime
from utils.logger import get_logger
from utils.base_widgets import (StyledCard, StyledDateEdit, StyledTimeEdit, StyledSpinBox,
                                StyledButton, StyledListWidget, TitleLabel, StyledInput, StyledComboBox)
from styles import BloodPressureStyles, BaseStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('blood_pressure_monitor')


class BloodPressureMonitorScreen(QWidget, UserMixin):
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
        title = TitleLabel("Моніторинг артеріального тиску", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Контролюйте артеріальний тиск під час вагітності")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Інформація без фону
        info_title = QLabel("🩺 Важливо знати")
        info_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(info_title)

        info_text = """• Нормальний тиск під час вагітності: 110-120/70-80 мм рт.ст.
• Регулярне вимірювання допомагає виявити ускладнення
• Підвищений тиск може бути ознакою прееклампсії
• При тиску 140/90 і вище - негайно до лікаря"""

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

        # Верхній тиск
        systolic_label = QLabel("📈 Верхній тиск:")
        systolic_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        systolic_label.setMinimumHeight(24)

        self.systolic_spin = StyledSpinBox(80, 200)
        self.systolic_spin.setValue(120)
        self.systolic_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.systolic_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.systolic_spin.setMinimumHeight(24)
        self.systolic_spin.setMaximumHeight(40)

        form_layout.addRow(systolic_label, self.systolic_spin)

        # Нижній тиск
        diastolic_label = QLabel("📉 Нижній тиск:")
        diastolic_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        diastolic_label.setMinimumHeight(24)

        self.diastolic_spin = StyledSpinBox(50, 120)
        self.diastolic_spin.setValue(80)
        self.diastolic_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.diastolic_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.diastolic_spin.setMinimumHeight(24)
        self.diastolic_spin.setMaximumHeight(40)

        form_layout.addRow(diastolic_label, self.diastolic_spin)

        # Пульс
        pulse_label = QLabel("💓 Пульс:")
        pulse_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        pulse_label.setMinimumHeight(24)

        self.pulse_spin = StyledSpinBox(40, 200)
        self.pulse_spin.setValue(75)
        self.pulse_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.pulse_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.pulse_spin.setMinimumHeight(24)
        self.pulse_spin.setMaximumHeight(40)

        form_layout.addRow(pulse_label, self.pulse_spin)

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
        save_btn.setStyleSheet(BloodPressureStyles.pressure_button())
        save_btn.clicked.connect(self.save_pressure)
        main_layout.addWidget(save_btn)

        # Відступ
        main_layout.addSpacing(20)

        # Історія без рамки
        history_title = QLabel("📊 Історія вимірювань")
        history_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(history_title)

        # Період відображення
        period_layout = QHBoxLayout()
        period_label = QLabel("📅 Показати за:")
        period_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")

        self.period_spin = StyledSpinBox(7, 90, " днів")
        self.period_spin.setValue(30)
        self.period_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.period_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.period_spin.setMinimumHeight(24)
        self.period_spin.setMaximumHeight(40)
        self.period_spin.valueChanged.connect(self.load_pressure_records)

        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_spin)
        period_layout.addStretch()

        main_layout.addLayout(period_layout)

        self.pressure_list = StyledListWidget()
        self.pressure_list.setStyleSheet("""
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
        self.pressure_list.setWordWrap(True)
        self.pressure_list.setTextElideMode(Qt.TextElideMode.ElideNone)
        main_layout.addWidget(self.pressure_list)

        # Розтягуючий spacer
        main_layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        if self.init_data_controller():
            self.load_pressure_records()

    def load_pressure_records(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для перегляду записів")
            return

        try:
            user_id = self.get_current_user_id()
            days = self.period_spin.value() if hasattr(self, 'period_spin') else 30
            records = self.data_controller.db.get_blood_pressure(user_id, days)
            self.pressure_list.clear()

            for record in records:
                item_text = f"{record['date']} {record['time']}: {record['systolic']}/{record['diastolic']} мм рт.ст."
                if record['pulse']:
                    item_text += f", пульс: {record['pulse']}"
                if record['notes']:
                    item_text += f" - {record['notes']}"
                self.pressure_list.addItem(item_text)

            logger.info(f"Завантажено {len(records)} записів про тиск за {days} днів для користувача {user_id}")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося завантажити записи про тиск: {str(e)}")
            logger.error(f"Помилка при завантаженні записів про тиск для користувача {user_id}: {str(e)}")

    def save_pressure(self):
        if not self.init_data_controller():
            show_warning(self, "Помилка", "Необхідно увійти в систему для збереження записів")
            return

        try:
            user_id = self.get_current_user_id()
            date_str = self.date_edit.date().toString("yyyy-MM-dd")
            time_text = self.time_edit.text().strip()
            
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
                
            systolic = self.systolic_spin.value()
            diastolic = self.diastolic_spin.value()
            pulse = self.pulse_spin.value()
            notes = self.notes_edit.text().strip()

            if systolic <= diastolic:
                show_warning(self, "Помилка валідації",
                                    "Верхній тиск повинен бути більшим за нижній.")
                return

            self.data_controller.db.add_blood_pressure(date_str, time_str, systolic, diastolic, pulse, notes,
                                                       user_id)
            self.notes_edit.clear()
            self.load_pressure_records()

            show_info(self, "Успіх", "Запис збережено")
            logger.info(
                f"Збережено новий запис тиску для користувача {user_id}: {date_str} {time_str}, {systolic}/{diastolic}, пульс: {pulse}")

            if systolic >= 140 or diastolic >= 90:
                show_warning(self, "Увага! Підвищений тиск",
                                    f"Ваш тиск {systolic}/{diastolic} мм рт.ст. перевищує норму.\n"
                                    "Рекомендується проконсультуватися з лікарем.")

        except Exception as e:
            show_error(self, "Помилка", f"Не вдалося зберегти запис: {str(e)}")
            logger.error(f"Помилка при збереженні запису тиску для користувача {user_id}: {str(e)}")