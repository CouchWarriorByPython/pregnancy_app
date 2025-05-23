from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QMessageBox
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledDoubleSpinBox, StyledSpinBox,
                                StyledButton, TitleLabel, StyledScrollArea)
from utils.styles import Styles
from datetime import datetime
from controllers.data_controller import DataController

logger = get_logger('user_info_screen')


class UserInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.user_name_input = StyledInput("Введіть ваше ім'я")
        self.birth_date_edit = StyledDateEdit()
        self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))

        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.weight_spin.setValue(60.0)

        self.height_spin = StyledSpinBox(100, 220, " см")
        self.height_spin.setValue(165)

        self.cycle_spin = StyledSpinBox(21, 35, " днів")
        self.cycle_spin.setValue(28)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        scroll_area = StyledScrollArea()
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)

        title = TitleLabel("Інформація про вас")
        form_layout.addWidget(title)

        profile_form = self._create_profile_form()
        form_layout.addLayout(profile_form)
        form_layout.addStretch(1)

        finish_btn = StyledButton("Завершити")
        finish_btn.setMinimumHeight(50)
        finish_btn.clicked.connect(self._on_finish_clicked)
        form_layout.addWidget(finish_btn)

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

    def _create_profile_form(self):
        form = QFormLayout()
        form.setSpacing(15)

        fields = [
            ("Ваше ім'я:", self.user_name_input),
            ("Дата народження:", self.birth_date_edit),
            ("Вага до вагітності:", self.weight_spin),
            ("Зріст:", self.height_spin),
            ("Середня тривалість циклу:", self.cycle_spin)
        ]

        for label_text, widget in fields:
            form.addRow(label_text, widget)

        return form

    def _get_current_user_id(self):
        """Отримуємо ID поточного користувача"""
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        return None

    def _load_user_data(self):
        """Завантажуємо дані користувача якщо вони є"""
        user_id = self._get_current_user_id()
        if not user_id:
            logger.info("Користувач не авторизований, залишаємо дефолтні значення")
            return

        try:
            self.data_controller = DataController(user_id)
            profile = self.data_controller.user_profile

            if not profile:
                logger.info("Профіль не знайдено, залишаємо дефолтні значення")
                return

            self.user_name_input.setText(profile.name or "")

            if profile.birth_date:
                qdate = QDate(profile.birth_date.year, profile.birth_date.month, profile.birth_date.day)
                self.birth_date_edit.setDate(qdate)

            self.weight_spin.setValue(profile.weight_before_pregnancy or 60.0)
            self.height_spin.setValue(profile.height or 165)
            self.cycle_spin.setValue(profile.cycle_length or 28)

            logger.info(f"Дані користувача {profile.name} завантажено")
        except Exception as e:
            logger.error(f"Помилка при завантаженні даних користувача: {e}")

    def _on_finish_clicked(self):
        logger.info("Натиснуто кнопку 'Завершити'")

        user_id = self._get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "Помилка", "Користувач не авторизований")
            return

        birth_date = self.birth_date_edit.date()
        birth_date_obj = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()

        user_data = {
            "name": self.user_name_input.text().strip(),
            "birth_date": birth_date_obj.isoformat(),
            "weight_before_pregnancy": self.weight_spin.value(),
            "height": self.height_spin.value(),
            "cycle_length": self.cycle_spin.value()
        }

        try:
            # Ініціалізуємо DataController з правильним user_id
            if not self.data_controller:
                self.data_controller = DataController(user_id)

            profile = self.data_controller.user_profile
            if not profile:
                QMessageBox.critical(self, "Помилка", "Не вдалося знайти профіль користувача")
                return

            # Оновлюємо дані профілю
            profile.name = user_data["name"]
            profile.birth_date = birth_date_obj
            profile.weight_before_pregnancy = user_data["weight_before_pregnancy"]
            profile.height = user_data["height"]
            profile.cycle_length = user_data["cycle_length"]

            self.data_controller.save_user_profile()

            logger.info("Профіль користувача збережено")
            self.proceed_signal.emit(user_data)
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка при збереженні даних: {str(e)}")
            logger.error(f"Помилка при збереженні даних користувача: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        self._load_user_data()