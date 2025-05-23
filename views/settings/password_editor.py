from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QFrame, QMessageBox
from controllers.auth_controller import AuthController
from utils.logger import get_logger
from utils.base_widgets import StyledInput, StyledButton, TitleLabel
from utils.styles import Styles

logger = get_logger('password_editor')


class PasswordEditor(QWidget):
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

        self.new_password_input = StyledInput()
        self.new_password_input.setEchoMode(self.new_password_input.EchoMode.Password)
        self.new_password_input.setPlaceholderText("Введіть новий пароль")

        self.confirm_password_input = StyledInput()
        self.confirm_password_input.setEchoMode(self.confirm_password_input.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Підтвердіть новий пароль")

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        title = TitleLabel("Зміна паролю", 18)
        main_layout.addWidget(title)

        form_frame = self._create_form_frame()
        main_layout.addWidget(form_frame)
        main_layout.addStretch(1)

        change_btn = StyledButton("Змінити пароль")
        change_btn.setMinimumHeight(50)
        change_btn.clicked.connect(self.change_password)
        main_layout.addWidget(change_btn)

    def _create_form_frame(self):
        form_frame = QFrame()
        form_frame.setStyleSheet(Styles.card_frame())
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(15, 15, 15, 15)

        fields = [
            ("Поточний пароль:", self.current_password_input),
            ("Новий пароль:", self.new_password_input),
            ("Підтвердіть новий пароль:", self.confirm_password_input)
        ]

        for label_text, widget in fields:
            widget.setMinimumHeight(40)
            form_layout.addRow(label_text, widget)

        return form_frame

    def change_password(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Помилка", "Заповніть всі поля")
            return

        if len(new_password) < 6:
            QMessageBox.warning(self, "Помилка", "Новий пароль повинен містити мінімум 6 символів")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Помилка", "Новий пароль та підтвердження не співпадають")
            return

        if current_password == new_password:
            QMessageBox.warning(self, "Помилка", "Новий пароль повинен відрізнятися від поточного")
            return

        user_id = self._get_current_user_id()
        if not user_id:
            QMessageBox.critical(self, "Помилка", "Користувач не авторизований")
            return

        try:
            success = self.auth_controller.change_password(user_id, current_password, new_password)
            if success:
                QMessageBox.information(self, "Успіх", "Пароль успішно змінено")
                self.current_password_input.clear()
                self.new_password_input.clear()
                self.confirm_password_input.clear()
                logger.info("Пароль успішно змінено")
            else:
                QMessageBox.warning(self, "Помилка", "Неправильний поточний пароль")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка зміни паролю: {str(e)}")
            logger.error(f"Помилка зміни паролю: {str(e)}")

    def _get_current_user_id(self):
        if hasattr(self.parent, 'current_user_id'):
            if callable(self.parent.current_user_id):
                return self.parent.current_user_id()
            else:
                return self.parent.current_user_id
        # Якщо parent має parent (MainWindow)
        if hasattr(self.parent, 'parent') and hasattr(self.parent.parent, 'current_user_id'):
            return self.parent.parent.current_user_id
        return None