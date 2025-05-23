from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from utils.base_widgets import StyledInput, StyledButton, TitleLabel
from utils.styles import Styles
from controllers.auth_controller import AuthController
from utils.logger import get_logger

logger = get_logger('login_screen')


class LoginScreen(QWidget):
    login_success = pyqtSignal(dict)
    switch_to_register = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        title = TitleLabel("Вхід в акаунт", 24)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Введіть ваші дані для входу")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(Styles.text_secondary())
        subtitle.setFont(QFont('Arial', 14))
        main_layout.addWidget(subtitle)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.email_input = StyledInput("Електронна пошта")
        self.email_input.setMinimumHeight(50)
        main_layout.addWidget(self.email_input)

        main_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        login_btn = StyledButton("Увійти")
        login_btn.setMinimumHeight(55)
        login_btn.clicked.connect(self.login)
        main_layout.addWidget(login_btn)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        switch_text = QLabel("Немає акаунту?")
        switch_text.setStyleSheet(Styles.text_secondary())

        switch_btn = StyledButton("Зареєструватись", "secondary")
        switch_btn.setMinimumHeight(40)
        switch_btn.clicked.connect(self.switch_to_register.emit)

        switch_layout.addWidget(switch_text)
        switch_layout.addWidget(switch_btn)
        main_layout.addLayout(switch_layout)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def login(self):
        email = self.email_input.text().strip()

        if not email:
            QMessageBox.warning(self, "Помилка", "Введіть електронну пошту")
            return

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Помилка", "Введіть коректну електронну пошту")
            return

        try:
            user = self.auth_controller.login(email)
            if user:
                if user.is_verified:
                    self.login_success.emit({"user_id": user.id, "email": user.email})
                    logger.info(f"Успішний вхід користувача {email}")
                else:
                    QMessageBox.information(self, "Увага",
                                            "Акаунт не підтверджено. Перейдіть до реєстрації для підтвердження.")
            else:
                QMessageBox.warning(self, "Помилка", "Користувача з такою поштою не знайдено")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка входу: {str(e)}")
            logger.error(f"Помилка входу: {str(e)}")

    def is_valid_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None