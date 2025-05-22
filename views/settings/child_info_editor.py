from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QComboBox, QPushButton, QFormLayout, QFrame)
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from utils.logger import get_logger

logger = get_logger('child_info_editor')

class ChildInfoEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_controller = DataController()
        self.setup_ui()
        self.load_child_data()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = QLabel("Інформація про дитину")
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF8C00;")
        main_layout.addWidget(title)

        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #222222; border-radius: 15px; padding: 15px;")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)

        self.name_edit = QLineEdit()
        self.name_edit.setMinimumHeight(40)
        self.name_edit.setStyleSheet(
            "background-color: #333333; color: white; padding: 8px; border: none; border-radius: 5px;")
        form_layout.addRow("Ім'я дитини:", self.name_edit)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Невідомо", "Хлопчик", "Дівчинка"])
        self.gender_combo.setMinimumHeight(40)
        self.gender_combo.setStyleSheet(
            "background-color: #333333; color: white; padding: 8px; border: none; border-radius: 5px;")
        form_layout.addRow("Стать дитини:", self.gender_combo)

        main_layout.addWidget(form_frame)
        main_layout.addStretch(1)

        save_btn = QPushButton("Зберегти зміни")
        save_btn.setMinimumHeight(50)
        save_btn.setStyleSheet("""
            background-color: #FF8C00;
            border: none;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)
        save_btn.clicked.connect(self.save_child_data)
        main_layout.addWidget(save_btn)

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