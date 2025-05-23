from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from utils.base_widgets import StyledInput, StyledButton, TitleLabel
from styles.auth import VerificationStyles
from controllers.auth_controller import AuthController
from utils.logger import get_logger

logger = get_logger('verification_screen')


class VerificationScreen(QWidget):
    verification_success = pyqtSignal(dict)
    back_to_register = pyqtSignal()

    def __init__(self, email=None, parent=None):
        super().__init__(parent)
        self.email = email
        self.auth_controller = AuthController()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(VerificationStyles.main_container())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        title = TitleLabel("Підтвердження пошти", 24)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(VerificationStyles.title_label())
        main_layout.addWidget(title)

        self.subtitle = QLabel(f"Код підтвердження надіслано на\n{self.email or 'вашу пошту'}")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet(VerificationStyles.code_description())
        self.subtitle.setFont(QFont('Arial', 14))
        main_layout.addWidget(self.subtitle)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        self.code_input = StyledInput("Введіть 6-значний код")
        self.code_input.setMinimumHeight(50)
        self.code_input.setMaxLength(6)
        self.code_input.setStyleSheet(VerificationStyles.verification_code_input())
        main_layout.addWidget(self.code_input)

        main_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        verify_btn = StyledButton("Підтвердити")
        verify_btn.setMinimumHeight(55)
        verify_btn.setStyleSheet(VerificationStyles.auth_button_large())
        verify_btn.clicked.connect(self.verify)
        main_layout.addWidget(verify_btn)

        resend_btn = StyledButton("Надіслати код повторно", "secondary")
        resend_btn.setMinimumHeight(45)
        resend_btn.setStyleSheet(VerificationStyles.resend_button())
        resend_btn.clicked.connect(self.resend_code)
        main_layout.addWidget(resend_btn)

        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        back_btn = StyledButton("Назад", "secondary")
        back_btn.setMinimumHeight(40)
        back_btn.setStyleSheet(VerificationStyles.back_button())
        back_btn.clicked.connect(self.back_to_register.emit)
        main_layout.addWidget(back_btn)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def set_email(self, email):
        self.email = email
        self.subtitle.setText(f"Код підтвердження надіслано на\n{email}")

    def verify(self):
        code = self.code_input.text().strip()

        if not code:
            QMessageBox.warning(self, "Помилка", "Введіть код підтвердження")
            return

        if len(code) != 6:
            QMessageBox.warning(self, "Помилка", "Код повинен містити 6 цифр")
            return

        try:
            user = self.auth_controller.verify_email(self.email, code)
            if user:
                self.verification_success.emit({"user_id": user.id, "email": user.email})
                logger.info(f"Успішне підтвердження пошти {self.email}")
            else:
                QMessageBox.warning(self, "Помилка", "Невірний код підтвердження")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка підтвердження: {str(e)}")
            logger.error(f"Помилка підтвердження: {str(e)}")

    def resend_code(self):
        try:
            success = self.auth_controller.resend_verification_code(self.email)
            if success:
                QMessageBox.information(self, "Успіх", "Код підтвердження надіслано повторно")
                logger.info(f"Повторне надсилання коду для {self.email}")
            else:
                QMessageBox.warning(self, "Помилка", "Не вдалося надіслати код повторно")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Помилка відправки коду: {str(e)}")
            logger.error(f"Помилка відправки коду: {str(e)}")