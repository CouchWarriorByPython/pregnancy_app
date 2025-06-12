from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame, QMessageBox
from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledComboBox, StyledButton, TitleLabel
from styles import ChildInfoEditorStyles

logger = get_logger('child_info_editor')


class ChildInfoEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.name_edit = StyledInput("Введіть ім'я дитини")
        self.gender_combo = StyledComboBox(["❓ Невідомо", "👦 Хлопчик", "👧 Дівчинка"])

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_container = QWidget()
        title_container.setStyleSheet(ChildInfoEditorStyles.title_container())

        title_layout = QVBoxLayout(title_container)
        title = TitleLabel("👶 Інформація про дитину", 20)
        title.setStyleSheet(ChildInfoEditorStyles.section_title())
        title_layout.addWidget(title)

        subtitle = QLabel("Дані про вашого малюка")
        subtitle.setStyleSheet(ChildInfoEditorStyles.section_subtitle())
        title_layout.addWidget(subtitle)

        main_layout.addWidget(title_container)

        form_frame = self._create_form_frame()
        main_layout.addWidget(form_frame)

        save_btn = StyledButton("💾 Зберегти зміни")
        save_btn.setMinimumHeight(56)
        save_btn.setStyleSheet(ChildInfoEditorStyles.save_button())
        save_btn.clicked.connect(self.save_child_data)
        main_layout.addWidget(save_btn)

    def _create_form_frame(self):
        form_frame = QFrame()
        form_frame.setStyleSheet(ChildInfoEditorStyles.form_frame())
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(20)

        fields = [
            ("👶 Ім'я дитини:", self.name_edit),
            ("⚧️ Стать дитини:", self.gender_combo)
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(ChildInfoEditorStyles.field_label())
            widget.setMinimumHeight(48)

            if widget == self.gender_combo:
                widget.setStyleSheet(ChildInfoEditorStyles.gender_combo())

            form_layout.addRow(label, widget)

        return form_frame

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'current_user_id'):
            return self.parent.parent.current_user_id
        return None

    def load_child_data(self):
        user_id = self._get_current_user_id()
        if not user_id:
            logger.warning("Користувач не авторизований")
            self.name_edit.setText("")
            self.gender_combo.setCurrentText("❓ Невідомо")
            return

        self.data_controller = DataController(user_id)

        if not self.data_controller.pregnancy_data:
            self.name_edit.setText("")
            self.gender_combo.setCurrentText("❓ Невідомо")
            return

        child_info = self.data_controller.get_child_info()
        self.name_edit.setText(child_info.get("name", ""))

        gender = child_info.get("gender", "Невідомо")

        gender_mapping = {
            "Невідомо": "❓ Невідомо",
            "Хлопчик": "👦 Хлопчик",
            "Дівчинка": "👧 Дівчинка"
        }

        display_gender = gender_mapping.get(gender, "❓ Невідомо")
        index = self.gender_combo.findText(display_gender)
        if index >= 0:
            self.gender_combo.setCurrentIndex(index)

    def save_child_data(self):
        if not self.data_controller or not self.data_controller.pregnancy_data:
            QMessageBox.warning(self, "❌ Помилка", "Неможливо зберегти дані про дитину - користувач не авторизований")
            return

        gender_text = self.gender_combo.currentText()
        gender_mapping = {
            "❓ Невідомо": "Невідомо",
            "👦 Хлопчик": "Хлопчик",
            "👧 Дівчинка": "Дівчинка"
        }

        child_data = {
            "name": self.name_edit.text(),
            "gender": gender_mapping.get(gender_text, "Невідомо"),
            "first_labour": True
        }

        try:
            success = self.data_controller.save_child_info(child_data)
            if success:
                QMessageBox.information(self, "✅ Успіх", "Інформація про дитину успішно збережена!")
                logger.info("Інформація про дитину успішно збережена")
            else:
                QMessageBox.warning(self, "❌ Помилка", "Не вдалося зберегти інформацію про дитину")
                logger.error("Помилка при збереженні інформації про дитину")
        except Exception as e:
            QMessageBox.critical(self, "❌ Помилка", f"Помилка збереження: {str(e)}")
            logger.error(f"Помилка збереження даних про дитину: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        self.load_child_data()