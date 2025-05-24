from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from utils.base_widgets import StyledInput, StyledButton, TitleLabel
from styles.auth import RegisterStyles
from controllers.auth_controller import AuthController
from utils.logger import get_logger

logger = get_logger('register_screen')


class RegisterScreen(QWidget):
    registration_success = pyqtSignal(str)
    switch_to_login = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(RegisterStyles.main_container())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        title = TitleLabel("Реєстрація", 24)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(RegisterStyles.title_label())
        main_layout.addWidget(title)

        subtitle = QLabel("Створіть новий акаунт")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(RegisterStyles.subtitle_label())
        subtitle.setFont(QFont('Arial', 14))
        main_layout.addWidget(subtitle)

        main_layout.addItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.email_input = StyledInput("Електронна пошта")
        self.email_input.setMinimumHeight(50)
        self.email_input.setStyleSheet(RegisterStyles.auth_input())
        main_layout.addWidget(self.email_input)

        self.name_input = StyledInput("Ваше ім'я")
        self.name_input.setMinimumHeight(50)
        self.name_input.setStyleSheet(RegisterStyles.auth_input())
        main_layout.addWidget(self.name_input)

        self.password_input = StyledInput("Пароль")
        self.password_input.setMinimumHeight(50)
        self.password_input.setEchoMode(self.password_input.EchoMode.Password)
        self.password_input.setStyleSheet(RegisterStyles.auth_input())
        main_layout.addWidget(self.password_input)

        self.password_confirm_input = StyledInput("Підтвердіть пароль")
        self.password_confirm_input.setMinimumHeight(50)
        self.password_confirm_input.setEchoMode(self.password_confirm_input.EchoMode.Password)
        self.password_confirm_input.setStyleSheet(RegisterStyles.auth_input())
        main_layout.addWidget(self.password_confirm_input)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        register_btn = StyledButton("Зареєструватись")
        register_btn.setMinimumHeight(55)
        register_btn.setStyleSheet(RegisterStyles.auth_button_large())
        register_btn.clicked.connect(self.register)
        main_layout.addWidget(register_btn)

        main_layout.addItem(QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        switch_text = QLabel("Вже є акаунт?")
        switch_text.setStyleSheet(RegisterStyles.subtitle_label())

        switch_btn = StyledButton("Увійти", "secondary")
        switch_btn.setMinimumHeight(40)
        switch_btn.setStyleSheet(RegisterStyles.switch_button())
        switch_btn.clicked.connect(self.switch_to_login.emit)

        switch_layout.addWidget(switch_text)
        switch_layout.addWidget(switch_btn)
        main_layout.addLayout(switch_layout)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def register(self):
        email = self.email_input.text().strip()
        name = self.name_input.text().strip()
        password = self.password_input.text()
        password_confirm = self.password_confirm_input.text()

        if not email or not name or not password:
            QMessageBox.warning(self, "Помилка", "Заповніть всі поля")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Помилка", "Введіть коректну електронну пошту")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Помилка", "Пароль повинен містити мінімум 6 символів")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "Помилка", "Паролі не співпадають")
            return

        try:
            success = self.auth_controller.register(email, name, password)
            if success:
                self.registration_success.emit(email)
                logger.info(f"Успішна реєстрація користувача {email}")
            else:
                QMessageBox.warning(self, "Помилка", "Користувач з такою поштою вже існує")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка реєстрації: {str(e)}")
            logger.error(f"Помилка реєстрації: {str(e)}")

    def is_valid_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None