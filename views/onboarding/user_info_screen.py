from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout
from PyQt6.QtCore import pyqtSignal, QDate
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledDoubleSpinBox, StyledSpinBox,
                                StyledCheckBox, StyledButton, TitleLabel, StyledScrollArea)
from utils.styles import Styles
from datetime import datetime
from controllers.data_controller import DataController

logger = get_logger('user_info_screen')


class UserInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_controller = DataController()
        self._init_controls()
        self._setup_ui()
        self._load_user_data()

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

        self.diet_checkboxes = {}

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

        diet_section = self._create_diet_section()
        form_layout.addWidget(diet_section)
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

    def _create_diet_section(self):
        from PyQt6.QtWidgets import QLabel

        section = QWidget()
        layout = QVBoxLayout(section)

        diet_label = QLabel("Дієтичні вподобання:")
        diet_label.setStyleSheet(Styles.text_primary())
        layout.addWidget(diet_label)

        diet_options = ["Вегетаріанство", "Веганство", "Безглютенова дієта", "Низьколактозна дієта"]
        for option in diet_options:
            checkbox = StyledCheckBox(option)
            self.diet_checkboxes[option] = checkbox
            layout.addWidget(checkbox)

        return section

    def _load_user_data(self):
        try:
            profile = self.data_controller.user_profile
            if not profile:
                return

            self.user_name_input.setText(profile.name or "")

            if profile.birth_date:
                qdate = QDate(profile.birth_date.year, profile.birth_date.month, profile.birth_date.day)
                self.birth_date_edit.setDate(qdate)

            self.weight_spin.setValue(profile.weight_before_pregnancy or 60.0)
            self.height_spin.setValue(profile.height or 165)
            self.cycle_spin.setValue(profile.cycle_length or 28)

            diet_preferences = self.data_controller.db.get_diet_preferences()
            for option, checkbox in self.diet_checkboxes.items():
                checkbox.setChecked(option in diet_preferences)

            logger.info(f"Дані користувача {profile.name} завантажено")
        except Exception as e:
            logger.error(f"Помилка при завантаженні даних користувача: {e}")

    def _on_finish_clicked(self):
        logger.info("Натиснуто кнопку 'Завершити'")

        birth_date = self.birth_date_edit.date()
        birth_date_obj = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()

        diet_preferences = [option for option, checkbox in self.diet_checkboxes.items()
                            if checkbox.isChecked()]

        user_data = {
            "name": self.user_name_input.text().strip(),
            "birth_date": birth_date_obj.isoformat(),
            "weight_before_pregnancy": self.weight_spin.value(),
            "height": self.height_spin.value(),
            "cycle_length": self.cycle_spin.value(),
            "diet_preferences": diet_preferences
        }

        try:
            profile = self.data_controller.user_profile
            profile.name = user_data["name"]
            profile.birth_date = birth_date_obj
            profile.weight_before_pregnancy = user_data["weight_before_pregnancy"]
            profile.height = user_data["height"]
            profile.cycle_length = user_data["cycle_length"]

            self.data_controller.db.update_diet_preferences(user_data["diet_preferences"])
            self.data_controller.save_user_profile()

            logger.info("Профіль користувача збережено")
            self.proceed_signal.emit(user_data)
        except Exception as e:
            logger.error(f"Помилка при збереженні даних користувача: {e}")