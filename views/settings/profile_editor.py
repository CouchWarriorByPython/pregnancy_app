from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QFrame
from PyQt6.QtCore import QDate
from controllers.data_controller import DataController
from datetime import datetime
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledSpinBox, StyledDoubleSpinBox,
                                StyledButton, StyledScrollArea, TitleLabel)

logger = get_logger('profile_editor')


class ProfileEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Ініціалізація редактора профілю")
        self.data_controller = DataController()
        self._init_controls()
        self._setup_ui()
        self.load_profile_data()

    def _init_controls(self):
        self.name_edit = StyledInput()
        self.email_edit = StyledInput()
        self.email_edit.setEnabled(False)  # Email не можна редагувати
        self.birth_date_edit = StyledDateEdit()
        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.height_spin = StyledSpinBox(100, 220, " см")
        self.prev_pregnancies_spin = StyledSpinBox(0, 10)
        self.cycle_spin = StyledSpinBox(21, 35, " днів")

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = TitleLabel("Ваш профіль", 18)
        main_layout.addWidget(title)

        scroll_area = StyledScrollArea()
        form_widget = QWidget()
        self.form_layout = QFormLayout(form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)

        self._add_form_fields()

        save_btn = StyledButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_profile)

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area, 1)
        main_layout.addWidget(save_btn)

    def _add_form_fields(self):
        fields = [
            ("Електронна пошта:", self.email_edit),
            ("Ваше ім'я:", self.name_edit),
            ("Дата народження:", self.birth_date_edit),
            ("Вага до вагітності:", self.weight_spin),
            ("Зріст:", self.height_spin),
            ("Кількість попередніх вагітностей:", self.prev_pregnancies_spin),
            ("Середня тривалість циклу:", self.cycle_spin)
        ]

        for label, widget in fields:
            widget.setMinimumHeight(40)
            self.form_layout.addRow(label, widget)

    def load_profile_data(self):
        logger.info("Завантаження даних профілю")
        profile = self.data_controller.user_profile

        if not profile:
            logger.info("Профіль не знайдено, встановлюємо дефолтні значення")
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
        if not self.data_controller.user_profile:
            logger.warning("Неможливо зберегти профіль - користувач не авторизований")
            return

        logger.info("Зберігання змін у профілі")
        profile = self.data_controller.user_profile

        profile.name = self.name_edit.text()
        birth_date = self.birth_date_edit.date()
        profile.birth_date = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()
        profile.weight_before_pregnancy = self.weight_spin.value()
        profile.height = self.height_spin.value()
        profile.previous_pregnancies = self.prev_pregnancies_spin.value()
        profile.cycle_length = self.cycle_spin.value()

        self.data_controller.save_user_profile()

    def showEvent(self, event):
        super().showEvent(event)
        # Оновлюємо DataController при показі екрану
        if hasattr(self.parent(), 'current_user_id') and self.parent().current_user_id:
            self.data_controller = DataController(self.parent().current_user_id)
        self.load_profile_data()