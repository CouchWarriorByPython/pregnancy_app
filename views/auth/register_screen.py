from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from utils.base_widgets import StyledInput, StyledButton, TitleLabel
from utils.styles import Styles
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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        title = TitleLabel("Реєстрація", 24)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Створіть новий акаунт")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(Styles.text_secondary())
        subtitle.setFont(QFont('Arial', 14))
        main_layout.addWidget(subtitle)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.email_input = StyledInput("Електронна пошта")
        self.email_input.setMinimumHeight(50)
        main_layout.addWidget(self.email_input)

        self.name_input = StyledInput("Ваше ім'я")
        self.name_input.setMinimumHeight(50)
        main_layout.addWidget(self.name_input)

        main_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        register_btn = StyledButton("Зареєструватись")
        register_btn.setMinimumHeight(55)
        register_btn.clicked.connect(self.register)
        main_layout.addWidget(register_btn)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        switch_text = QLabel("Вже є акаунт?")
        switch_text.setStyleSheet(Styles.text_secondary())

        switch_btn = StyledButton("Увійти", "secondary")
        switch_btn.setMinimumHeight(40)
        switch_btn.clicked.connect(self.switch_to_login.emit)

        switch_layout.addWidget(switch_text)
        switch_layout.addWidget(switch_btn)
        main_layout.addLayout(switch_layout)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def register(self):
        email = self.email_input.text().strip()
        name = self.name_input.text().strip()

        if not email or not name:
            QMessageBox.warning(self, "Помилка", "Заповніть всі поля")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Помилка", "Введіть коректну електронну пошту")
            return

        try:
            success = self.auth_controller.register(email, name)
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