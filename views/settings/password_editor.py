from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QFrame, QMessageBox, QLabel
from controllers.auth_controller import AuthController
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledButton, TitleLabel, StyledScrollArea
from styles import PasswordEditorStyles, OnboardingScreenStyles
from utils.user_mixin import UserMixin

logger = get_logger('password_editor')


class PasswordEditor(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.auth_controller = AuthController()
        self._init_controls()
        self._setup_ui()

    def _init_controls(self):
        self.current_password_input = StyledInput()
        self.current_password_input.setEchoMode(self.current_password_input.EchoMode.Password)
        self.current_password_input.setPlaceholderText("Введіть поточний пароль")
        self.current_password_input.setStyleSheet(OnboardingScreenStyles.elegant_input())

        self.new_password_input = StyledInput()
        self.new_password_input.setEchoMode(self.new_password_input.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Введіть новий пароль")
        self.new_password_input.setStyleSheet(OnboardingScreenStyles.elegant_input())

        self.confirm_password_input = StyledInput()
        self.confirm_password_input.setEchoMode(self.confirm_password_input.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Підтвердіть новий пароль")
        self.confirm_password_input.setStyleSheet(OnboardingScreenStyles.elegant_input())

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(12)

        # Простий заголовок
        title = TitleLabel("🔐 Зміна паролю", 18)
        title.setStyleSheet("color: white; font-weight: 700; background: transparent; border: none;")
        main_layout.addWidget(title)

        subtitle = QLabel("Забезпечте безпеку вашого акаунту")
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent; border: none;")
        main_layout.addWidget(subtitle)

        # Поради без рамки
        info_title = QLabel("🛡️ Поради для безпечного паролю")
        info_title.setStyleSheet("color: white; font-weight: 700; font-size: 16px; background: transparent; border: none; margin-top: 8px;")
        main_layout.addWidget(info_title)

        tips_text = """- Використовуйте мінімум 8 символів
- Комбінуйте великі та малі літери
- Додавайте цифри та спеціальні символи
- Не використовуйте особисту інформацію
- Уникайте простих послідовностей"""

        tips_label = QLabel(tips_text)
        tips_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px; background: transparent; border: none;")
        tips_label.setWordWrap(True)
        main_layout.addWidget(tips_label)

        # Відступ
        main_layout.addSpacing(20)

        # Форма з підкресленими полями
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(20)
        form_layout.setHorizontalSpacing(20)

        fields = [
            ("🔒 Поточний пароль:", self.current_password_input),
            ("🆕 Новий пароль:", self.new_password_input),
            ("✅ Підтвердіть новий пароль:", self.confirm_password_input)
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet("color: white; font-size: 14px; font-weight: 600; background: transparent; border: none;")
            label.setMinimumHeight(24)
            
            widget.setMinimumHeight(24)
            widget.setMaximumHeight(40)
            
            form_layout.addRow(label, widget)

        main_layout.addLayout(form_layout)

        # Розтягуючий spacer
        main_layout.addStretch()

        # Компактна кнопка
        change_btn = StyledButton("🔒 Змінити")
        change_btn.setMinimumHeight(44)
        change_btn.setStyleSheet(PasswordEditorStyles.change_button())
        change_btn.clicked.connect(self.change_password)
        main_layout.addWidget(change_btn)

    def _create_security_info(self):
        info_frame = QFrame()
        info_frame.setStyleSheet(PasswordEditorStyles.security_info())

        layout = QVBoxLayout(info_frame)
        layout.setSpacing(12)

        info_title = QLabel("🛡️ Поради для безпечного паролю")
        info_title.setStyleSheet(PasswordEditorStyles.security_title())
        layout.addWidget(info_title)

        tips_text = """
- Використовуйте мінімум 8 символів
- Комбінуйте великі та малі літери
- Додавайте цифри та спеціальні символи
- Не використовуйте особисту інформацію
- Уникайте простих послідовностей
        """.strip()

        tips_label = QLabel(tips_text)
        tips_label.setStyleSheet(PasswordEditorStyles.security_tips())
        tips_label.setWordWrap(True)
        layout.addWidget(tips_label)

        return info_frame

    def _create_form_frame(self):
        form_frame = QFrame()
        form_frame.setStyleSheet(PasswordEditorStyles.form_frame())
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(24, 24, 24, 24)

        fields = [
            ("🔒 Поточний пароль:", self.current_password_input),
            ("🆕 Новий пароль:", self.new_password_input),
            ("✅ Підтвердіть новий пароль:", self.confirm_password_input)
        ]

        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setStyleSheet(PasswordEditorStyles.field_label())
            widget.setMinimumHeight(48)
            form_layout.addRow(label, widget)

        return form_frame

    def change_password(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        validation_error = self._validate_passwords(current_password, new_password, confirm_password)
        if validation_error:
            QMessageBox.warning(self, "❌ Помилка валідації", validation_error)
            return

        user_id = self.get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "❌ Помилка авторизації", "Користувач не авторизований")
            return

        try:
            success = self.auth_controller.change_password(user_id, current_password, new_password)
            if success:
                self._clear_form()
                QMessageBox.information(self, "✅ Успіх", "Пароль успішно змінено!\n\nВаш акаунт тепер більш захищений.")
                logger.info("Пароль успішно змінено")
            else:
                QMessageBox.warning(self, "❌ Помилка", "Неправильний поточний пароль")
        except Exception as e:
            QMessageBox.critical(self, "❌ Системна помилка", f"Помилка зміни паролю: {str(e)}")
            logger.error(f"Помилка зміни паролю: {str(e)}")

    def _validate_passwords(self, current_password, new_password, confirm_password):
        if not all([current_password, new_password, confirm_password]):
            return "Заповніть всі поля"

        if len(new_password) < 8:
            return "Новий пароль повинен містити мінімум 8 символів"

        if len(new_password) > 128:
            return "Новий пароль занадто довгий (максимум 128 символів)"

        if new_password != confirm_password:
            return "Новий пароль та підтвердження не співпадають"

        if current_password == new_password:
            return "Новий пароль повинен відрізнятися від поточного"

        if not self._check_password_strength(new_password):
            return ("Пароль занадто простий. Використовуйте комбінацію з:\n"
                   "• великих та малих літер\n"
                   "• цифр\n"
                   "• спеціальних символів")

        return None

    def _check_password_strength(self, password):
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        return sum([has_upper, has_lower, has_digit, has_special]) >= 3

    def _clear_form(self):
        self.current_password_input.clear()
        self.new_password_input.clear()
        self.confirm_password_input.clear()