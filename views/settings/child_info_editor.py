from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFormLayout, QFrame, QMessageBox, QRadioButton, QButtonGroup
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledComboBox, StyledButton, TitleLabel
from styles import ChildInfoEditorStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('child_info_editor')


class ChildInfoEditor(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.name_edit = StyledInput("Введіть ім'я дитини")
        self.name_edit.setStyleSheet(OnboardingScreenStyles.elegant_input())
        self.gender_group = QButtonGroup(self)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(12)

        # Простий заголовок
        title = TitleLabel("👶 Інформація про дитину", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Дані про вашого малюка")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Форма з підкресленими полями
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        form_layout.setHorizontalSpacing(20)

        # Ім'я дитини
        name_label = QLabel("👶 Ім'я дитини:")
        name_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        name_label.setMinimumHeight(24)

        self.name_edit.setMinimumHeight(24)
        self.name_edit.setMaximumHeight(40)

        form_layout.addRow(name_label, self.name_edit)

        main_layout.addLayout(form_layout)

        # Відступ між полями
        main_layout.addSpacing(16)

        # Стать дитини з радіокнопками як на онбордингу
        gender_label = QLabel("⚧️ Стать дитини:")
        gender_label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
        main_layout.addWidget(gender_label)

        # Відступ перед радіокнопками
        main_layout.addSpacing(8)

        # Радіокнопки як на першому екрані
        gender_options = [
            ("♂ Хлопчик", "Хлопчик"), 
            ("♀ Дівчинка", "Дівчинка"), 
            ("⚧ Ще не знаю", "Невідомо")
        ]

        for i, (text, value) in enumerate(gender_options):
            radio = QRadioButton(text)
            radio.setStyleSheet(OnboardingScreenStyles.gender_radio())
            radio.gender_value = value
            self.gender_group.addButton(radio, i)
            main_layout.addWidget(radio)

            # За замовчуванням вибираємо "Ще не знаю"
            if i == 2:
                radio.setChecked(True)

        # Розтягуючий spacer
        main_layout.addStretch()

        # Компактна кнопка
        save_btn = StyledButton("💾 Зберегти")
        save_btn.setMinimumHeight(44)
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

    def load_child_data(self):
        if not self.init_data_controller():
            logger.warning("Не вдалося ініціалізувати DataController")
            self.name_edit.setText("")
            self._set_gender_selection("Невідомо")
            return

        if not self.data_controller.pregnancy_data:
            self.name_edit.setText("")
            self._set_gender_selection("Невідомо")
            return

        child_info = self.data_controller.get_child_info()
        self.name_edit.setText(child_info.get("name", ""))

        gender = child_info.get("gender", "Невідомо")
        self._set_gender_selection(gender)

    def save_child_data(self):
        if not self.data_controller or not self.data_controller.pregnancy_data:
            QMessageBox.warning(self, "❌ Помилка", "Неможливо зберегти дані про дитину - користувач не авторизований")
            return

        child_data = {
            "name": self.name_edit.text(),
            "gender": self._get_selected_gender(),
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

    def _get_selected_gender(self):
        """Отримує вибрану стать з радіокнопок"""
        selected_button = self.gender_group.checkedButton()
        return selected_button.gender_value if selected_button else "Невідомо"

    def _set_gender_selection(self, gender):
        """Встановлює вибір статі в радіокнопках"""
        for button in self.gender_group.buttons():
            if hasattr(button, 'gender_value') and button.gender_value == gender:
                button.setChecked(True)
                return
        # Якщо не знайдено відповідну кнопку, вибираємо "Ще не знаю"
        for button in self.gender_group.buttons():
            if hasattr(button, 'gender_value') and button.gender_value == "Невідомо":
                button.setChecked(True)
                return

    def showEvent(self, event):
        super().showEvent(event)
        self.load_child_data()