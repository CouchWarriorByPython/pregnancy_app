from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QMessageBox, QHBoxLayout, QAbstractSpinBox
from PyQt6.QtCore import QDate
from datetime import datetime
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledSpinBox, StyledDoubleSpinBox,
                                StyledButton, StyledScrollArea, TitleLabel)
from styles import ProfileEditorStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('profile_editor')


class ProfileEditor(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.name_edit = StyledInput("Введіть ваше ім'я")
        self.name_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        
        self.email_edit = StyledInput("Електронна пошта")
        self.email_edit.setEnabled(False)
        self.email_edit.setStyleSheet("background: transparent; color: rgba(255, 255, 255, 0.6); border: none; border-bottom: 2px solid rgba(255, 255, 255, 0.3); border-radius: 0px; padding: 4px 4px 4px 4px; font-size: 16px; min-height: 20px; max-height: 24px;")

        self.birth_date_edit = StyledDateEdit()
        
        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.weight_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.weight_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        
        self.height_spin = StyledSpinBox(100, 220, " см")
        self.height_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.height_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        
        self.prev_pregnancies_spin = StyledSpinBox(0, 10)
        self.prev_pregnancies_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.prev_pregnancies_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())
        
        self.cycle_spin = StyledSpinBox(21, 35, " днів")
        self.cycle_spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cycle_spin.setStyleSheet(OnboardingScreenStyles.elegant_input())

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(12)

        # Простий заголовок без рамки
        title = TitleLabel("👤 Ваш профіль", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Персональна інформація та налаштування")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Форма зі скролом
        scroll_area = StyledScrollArea()
        form_widget = QWidget()
        form_widget.setStyleSheet("background: transparent; border: none;")
        self.form_layout = QFormLayout(form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(20)
        self.form_layout.setHorizontalSpacing(20)

        self._add_form_fields()

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area, 1)

        # Компактна кнопка збереження
        save_btn = StyledButton("💾 Зберегти")
        save_btn.setMinimumHeight(44)
        save_btn.setStyleSheet(ProfileEditorStyles.save_button())
        save_btn.clicked.connect(self.save_profile)
        main_layout.addWidget(save_btn)

    def _add_form_fields(self):
        fields = [
            ("📧 Електронна пошта:", self.email_edit),
            ("👤 Ваше ім'я:", self.name_edit),
            ("📅 Дата народження:", self.birth_date_edit),
            ("⚖️ Вага до вагітності:", self.weight_spin),
            ("📏 Зріст:", self.height_spin),
            ("🤱 Кількість попередніх вагітностей:", self.prev_pregnancies_spin),
            ("📊 Середня тривалість циклу:", self.cycle_spin)
        ]

        for label, widget in fields:
            widget.setMinimumHeight(24)
            widget.setMaximumHeight(40)

            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
            label_widget.setMinimumHeight(24)

            self.form_layout.addRow(label_widget, widget)

    def load_profile_data(self):
        if not self.init_data_controller():
            logger.warning("Не вдалося ініціалізувати DataController")
            return

        profile = self.data_controller.user_profile

        if not profile:
            self.email_edit.setText("")
            self.name_edit.setText("")
            self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))
            self.weight_spin.setValue(60.0)
            self.height_spin.setValue(165)
            self.prev_pregnancies_spin.setValue(0)
            self.cycle_spin.setValue(28)
            return

        self.email_edit.setText(profile.email or "")
        self.name_edit.setText(profile.name or "")

        if profile.birth_date:
            qdate = QDate(profile.birth_date.year, profile.birth_date.month, profile.birth_date.day)
            self.birth_date_edit.setDate(qdate)
        else:
            self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))

        self.weight_spin.setValue(profile.weight_before_pregnancy or 60.0)
        self.height_spin.setValue(profile.height or 165)
        self.prev_pregnancies_spin.setValue(profile.previous_pregnancies or 0)
        self.cycle_spin.setValue(profile.cycle_length or 28)

    def save_profile(self):
        if not self.data_controller or not self.data_controller.user_profile:
            QMessageBox.warning(self, "❌ Помилка", "Неможливо зберегти профіль - користувач не авторизований")
            return

        profile = self.data_controller.user_profile

        profile.name = self.name_edit.text()
        birth_date = self.birth_date_edit.date()
        profile.birth_date = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()
        profile.weight_before_pregnancy = self.weight_spin.value()
        profile.height = self.height_spin.value()
        profile.previous_pregnancies = self.prev_pregnancies_spin.value()
        profile.cycle_length = self.cycle_spin.value()

        try:
            self.data_controller.save_user_profile()
            QMessageBox.information(self, "✅ Успіх", "Профіль успішно збережено!")
        except Exception as e:
            QMessageBox.critical(self, "❌ Помилка", f"Помилка збереження: {str(e)}")
            logger.error(f"Помилка збереження профілю: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_profile_data()