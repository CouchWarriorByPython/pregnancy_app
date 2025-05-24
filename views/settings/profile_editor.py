from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QMessageBox
from PyQt6.QtCore import QDate
from controllers.data_controller import DataController
from datetime import datetime
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledSpinBox, StyledDoubleSpinBox,
                                StyledButton, StyledScrollArea, TitleLabel)
from styles.settings import SettingsStyles
from styles.base import BaseStyles

logger = get_logger('profile_editor')


class ProfileEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Ініціалізація редактора профілю")
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.name_edit = StyledInput()
        self.email_edit = StyledInput()
        self.email_edit.setEnabled(False)
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
        save_btn.setStyleSheet(SettingsStyles.save_button())
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
            label_widget = QLabel(label)
            label_widget.setStyleSheet(BaseStyles.text_primary())  # Тепер стиль не має фону
            self.form_layout.addRow(label_widget, widget)

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'current_user_id'):
            return self.parent.parent.current_user_id
        return None

    def load_profile_data(self):
        logger.info("Завантаження даних профілю")
        user_id = self._get_current_user_id()
        if not user_id:
            logger.warning("Користувач не авторизований")
            return

        self.data_controller = DataController(user_id)
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
        if not self.data_controller or not self.data_controller.user_profile:
            QMessageBox.warning(self, "Помилка", "Неможливо зберегти профіль - користувач не авторизований")
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

        try:
            self.data_controller.save_user_profile()
            QMessageBox.information(self, "Успіх", "Профіль успішно збережено")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка збереження: {str(e)}")
            logger.error(f"Помилка збереження профілю: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_profile_data()