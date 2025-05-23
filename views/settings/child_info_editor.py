from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledComboBox, StyledButton, TitleLabel
from utils.styles import Styles

logger = get_logger('child_info_editor')


class ChildInfoEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_controller = DataController()
        self._init_controls()
        self._setup_ui()
        self.load_child_data()

    def _init_controls(self):
        self.name_edit = StyledInput()
        self.gender_combo = StyledComboBox(["Невідомо", "Хлопчик", "Дівчинка"])

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = TitleLabel("Інформація про дитину", 18)
        main_layout.addWidget(title)

        form_frame = self._create_form_frame()
        main_layout.addWidget(form_frame)
        main_layout.addStretch(1)

        save_btn = StyledButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.clicked.connect(self.save_child_data)
        main_layout.addWidget(save_btn)

    def _create_form_frame(self):
        form_frame = QFrame()
        form_frame.setStyleSheet(Styles.card_frame())
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)

        fields = [
            ("Ім'я дитини:", self.name_edit),
            ("Стать дитини:", self.gender_combo)
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(Styles.text_primary())
            widget.setMinimumHeight(40)
            form_layout.addRow(label, widget)

        return form_frame

    def load_child_data(self):
        child_info = self.data_controller.get_child_info()
        self.name_edit.setText(child_info.get("name", ""))

        gender = child_info.get("gender", "Невідомо")
        index = self.gender_combo.findText(gender)
        if index >= 0:
            self.gender_combo.setCurrentIndex(index)

        logger.info("Завантажено дані про дитину")

    def save_child_data(self):
        child_data = {
            "name": self.name_edit.text(),
            "gender": self.gender_combo.currentText(),
            "first_labour": True
        }

        success = self.data_controller.save_child_info(child_data)
        if success:
            logger.info("Інформація про дитину успішно збережена")
        else:
            logger.error("Помилка при збереженні інформації про дитину")

    def showEvent(self, event):
        super().showEvent(event)
        self.data_controller = DataController()
        self.load_child_data()