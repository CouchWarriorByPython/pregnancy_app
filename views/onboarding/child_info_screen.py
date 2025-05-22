from PyQt6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QButtonGroup, QScrollArea, QLabel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledCheckBox, StyledButton, TitleLabel
from utils.styles import Styles

logger = get_logger('child_info_screen')

class ChildInfoScreen(QWidget):
    proceed_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.name_input = None
        self.first_labour_checkbox = None
        self.gender_group = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.scroll_area())

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)

        baby_title = TitleLabel("Інформація про дитину")
        form_layout.addWidget(baby_title)

        name_label = QLabel("Ім'я дитини")
        name_label.setStyleSheet(Styles.text_secondary())
        form_layout.addWidget(name_label)

        self.name_input = StyledInput("Залиште поле порожнім, якщо ви ще не обрали ім'я")
        form_layout.addWidget(self.name_input)

        self.first_labour_checkbox = StyledCheckBox("Це мої перші пологи")
        form_layout.addWidget(self.first_labour_checkbox)

        gender_label = QLabel("Стать дитини")
        gender_label.setFont(QFont('Arial', 16))
        gender_label.setStyleSheet(Styles.text_primary())
        form_layout.addWidget(gender_label)

        self.gender_group = QButtonGroup(self)
        gender_layout = QVBoxLayout()
        gender_layout.setSpacing(10)

        gender_options = [
            ("♂ Хлопчик", "Хлопчик"),
            ("♀ Дівчинка", "Дівчинка"),
            ("⚥ Ще не знаю", "Невідомо")
        ]

        for i, (text, value) in enumerate(gender_options):
            radio = QRadioButton(text)
            radio.setStyleSheet(Styles.radio_button())
            radio.gender_value = value
            self.gender_group.addButton(radio, i)
            gender_layout.addWidget(radio)

            if i == 2:
                radio.setChecked(True)

        form_layout.addLayout(gender_layout)
        form_layout.addStretch(1)

        next_btn = StyledButton("Далі")
        next_btn.clicked.connect(self.on_next_clicked)
        form_layout.addWidget(next_btn)

        scroll_area.setWidget(form_widget)
        main_layout.addWidget(scroll_area)

    def on_next_clicked(self):
        child_data = {
            "name": self.name_input.text().strip(),
            "first_labour": self.first_labour_checkbox.isChecked(),
            "gender": self.get_selected_gender()
        }

        logger.info(f"Дані дитини зібрані: {child_data}")
        self.proceed_signal.emit(child_data)

    def get_selected_gender(self):
        selected_button = self.gender_group.checkedButton()
        if selected_button:
            return selected_button.gender_value
        return "Невідомо"