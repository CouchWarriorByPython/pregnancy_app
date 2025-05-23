from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QRadioButton, QButtonGroup, QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledCheckBox, StyledButton, TitleLabel, StyledScrollArea
from styles.onboarding import ChildInfoStyles

logger = get_logger('child_info_screen')


class ChildInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.name_input = StyledInput("Залиште поле порожнім, якщо ви ще не обрали ім'я")
        self.name_input.setStyleSheet(ChildInfoStyles.onboarding_input())

        self.first_labour_checkbox = StyledCheckBox("Це мої перші пологи")
        self.first_labour_checkbox.setStyleSheet(ChildInfoStyles.first_labour_checkbox())

        self.gender_group = QButtonGroup(self)

    def _setup_ui(self):
        self.setStyleSheet(ChildInfoStyles.main_container())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        scroll_area = StyledScrollArea()
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)

        title = TitleLabel("Інформація про дитину")
        title.setStyleSheet(ChildInfoStyles.step_title())
        form_layout.addWidget(title)

        form_layout.addWidget(self._create_name_section())
        form_layout.addWidget(self.first_labour_checkbox)
        form_layout.addWidget(self._create_gender_section())
        form_layout.addStretch(1)

        next_btn = StyledButton("Далі")
        next_btn.setStyleSheet(ChildInfoStyles.onboarding_button())
        next_btn.clicked.connect(self._on_next_clicked)
        form_layout.addWidget(next_btn)

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

    def _create_name_section(self):
        section = QWidget()
        section.setStyleSheet(ChildInfoStyles.form_section())
        layout = QVBoxLayout(section)
        layout.setSpacing(10)

        name_label = QLabel("Ім'я дитини")
        name_label.setStyleSheet(ChildInfoStyles.field_label())
        layout.addWidget(name_label)
        layout.addWidget(self.name_input)

        return section

    def _create_gender_section(self):
        section = QWidget()
        section.setStyleSheet(ChildInfoStyles.gender_section())
        layout = QVBoxLayout(section)
        layout.setSpacing(10)

        gender_label = QLabel("Стать дитини")
        gender_label.setFont(QFont('Arial', 16))
        gender_label.setStyleSheet(ChildInfoStyles.section_label())
        layout.addWidget(gender_label)

        gender_options = [("♂ Хлопчик", "Хлопчик"), ("♀ Дівчинка", "Дівчинка"), ("⚥ Ще не знаю", "Невідомо")]

        for i, (text, value) in enumerate(gender_options):
            radio = QRadioButton(text)
            radio.setStyleSheet(ChildInfoStyles.gender_radio())
            radio.gender_value = value
            self.gender_group.addButton(radio, i)
            layout.addWidget(radio)

            if i == 2:
                radio.setChecked(True)

        return section

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        return None

    def _on_next_clicked(self):
        user_id = self._get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "Помилка", "Користувач не авторизований")
            return

        child_data = {
            "name": self.name_input.text().strip(),
            "first_labour": self.first_labour_checkbox.isChecked(),
            "gender": self._get_selected_gender()
        }
        logger.info(f"Дані дитини зібрані: {child_data}")
        self.proceed_signal.emit(child_data)

    def _get_selected_gender(self):
        selected_button = self.gender_group.checkedButton()
        return selected_button.gender_value if selected_button else "Невідомо"