from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QFrame, QMessageBox, QLabel
from controllers.auth_controller import AuthController
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledButton, TitleLabel, StyledScrollArea
from styles import PasswordEditorStyles
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
        self.current_password_input.setStyleSheet(PasswordEditorStyles.password_input())

        self.new_password_input = StyledInput()
        self.new_password_input.setEchoMode(self.new_password_input.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Введіть новий пароль")
        self.new_password_input.setStyleSheet(PasswordEditorStyles.password_input())

        self.confirm_password_input = StyledInput()
        self.confirm_password_input.setEchoMode(self.confirm_password_input.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Підтвердіть новий пароль")
        self.confirm_password_input.setStyleSheet(PasswordEditorStyles.password_input())

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_container = QWidget()
        title_container.setStyleSheet(PasswordEditorStyles.title_container())

        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title = TitleLabel("🔐 Зміна паролю", 20)
        title.setStyleSheet(PasswordEditorStyles.security_title())
        title_layout.addWidget(title)

        subtitle = QLabel("Забезпечте безпеку вашого акаунту")
        subtitle.setStyleSheet(PasswordEditorStyles.security_tips())
        title_layout.addWidget(subtitle)

        main_layout.addWidget(title_container)

        scroll_area = StyledScrollArea()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(20)

        security_info = self._create_security_info()
        content_layout.addWidget(security_info)

        form_frame = self._create_form_frame()
        content_layout.addWidget(form_frame)

        content_layout.addStretch(1)

        change_btn = StyledButton("🔒 Змінити пароль")
        change_btn.setMinimumHeight(56)
        change_btn.setStyleSheet(PasswordEditorStyles.change_button())
        change_btn.clicked.connect(self.change_password)
        content_layout.addWidget(change_btn)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area, 1)

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