from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSizePolicy, QFrame
from PyQt6.QtCore import QDate
from controllers.data_controller import DataController
from datetime import datetime
from utils.logger import get_logger
from utils.base_widgets import (StyledInput, StyledDateEdit, StyledSpinBox, StyledDoubleSpinBox,
                               StyledCheckBox, StyledButton, StyledScrollArea, TitleLabel)
from utils.styles import Styles

logger = get_logger('profile_editor')

class ProfileEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Ініціалізація редактора профілю")
        self.data_controller = DataController()
        self.setup_ui()
        self.load_profile_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = TitleLabel("Ваш профіль", 18)
        title.setStyleSheet(Styles.text_accent())
        main_layout.addWidget(title)

        scroll_area = StyledScrollArea()
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        form_widget = QWidget()
        form_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.form_layout = QFormLayout(form_widget)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(15)

        self.name_edit = StyledInput()
        self.name_edit.setMinimumHeight(40)
        self.form_layout.addRow("Ваше ім'я:", self.name_edit)

        self.birth_date_edit = StyledDateEdit()
        self.birth_date_edit.setMinimumHeight(40)
        self.form_layout.addRow("Дата народження:", self.birth_date_edit)

        self.weight_spin = StyledDoubleSpinBox(30.0, 150.0, 1, " кг")
        self.weight_spin.setMinimumHeight(40)
        self.form_layout.addRow("Вага до вагітності:", self.weight_spin)

        self.height_spin = StyledSpinBox(100, 220, " см")
        self.height_spin.setMinimumHeight(40)
        self.form_layout.addRow("Зріст:", self.height_spin)

        self.prev_pregnancies_spin = StyledSpinBox(0, 10)
        self.prev_pregnancies_spin.setMinimumHeight(40)
        self.form_layout.addRow("Кількість попередніх вагітностей:", self.prev_pregnancies_spin)

        self.cycle_spin = StyledSpinBox(21, 35, " днів")
        self.cycle_spin.setMinimumHeight(40)
        self.form_layout.addRow("Середня тривалість циклу:", self.cycle_spin)

        diet_frame = QFrame()
        diet_layout = QVBoxLayout(diet_frame)
        diet_layout.setContentsMargins(0, 0, 0, 0)
        diet_layout.setSpacing(5)

        self.diet_checkboxes = {}
        diet_options = ["Вегетаріанство", "Веганство", "Безглютенова дієта", "Низьколактозна дієта"]

        for option in diet_options:
            checkbox = StyledCheckBox(option)
            self.diet_checkboxes[option] = checkbox
            diet_layout.addWidget(checkbox)

        self.form_layout.addRow("Дієтичні вподобання:", diet_frame)

        save_btn = StyledButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_profile)

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area, 1)
        main_layout.addWidget(save_btn)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def showEvent(self, event):
        super().showEvent(event)
        self.data_controller = DataController()
        self.load_profile_data()

    def load_profile_data(self):
        logger.info("Завантаження даних профілю")
        profile = self.data_controller.user_profile

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

        diet_preferences = self.data_controller.db.get_diet_preferences()
        for option, checkbox in self.diet_checkboxes.items():
            checkbox.setChecked(option in diet_preferences)

        logger.info(f"Дані профілю користувача {profile.name} завантажено")

    def save_profile(self):
        logger.info("Зберігання змін у профілі")
        profile = self.data_controller.user_profile

        profile.name = self.name_edit.text()

        birth_date = self.birth_date_edit.date()
        profile.birth_date = datetime(birth_date.year(), birth_date.month(), birth_date.day()).date()

        profile.weight_before_pregnancy = self.weight_spin.value()
        profile.height = self.height_spin.value()
        profile.previous_pregnancies = self.prev_pregnancies_spin.value()
        profile.cycle_length = self.cycle_spin.value()

        diet_preferences = [option for option, checkbox in self.diet_checkboxes.items() if checkbox.isChecked()]
        self.data_controller.db.update_diet_preferences(diet_preferences)

        self.data_controller.save_user_profile()
        logger.info("Профіль успішно оновлено")