from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from styles import OnboardingScreenStyles


class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(OnboardingScreenStyles.main_container())

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 40, 20, 20)
        main_layout.setSpacing(15)

        title = QLabel("Щоденник вагітності")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title.setStyleSheet(OnboardingScreenStyles.step_title())
        main_layout.addWidget(title)

        welcome_text = QLabel(
            "Ласкаво просимо! Цей додаток допоможе вам відстежувати вагітність та отримувати корисну інформацію")
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_text.setWordWrap(True)
        welcome_text.setFont(QFont('Arial', 14))
        welcome_text.setStyleSheet(OnboardingScreenStyles.field_label())
        main_layout.addWidget(welcome_text)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setText("[Тут буде зображення]")
        image_label.setStyleSheet("background-color: #333333; min-height: 200px; border-radius: 15px;")
        main_layout.addWidget(image_label)

        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        button_layout = QVBoxLayout()

        start_btn = QPushButton("Почати користування")
        start_btn.setMinimumHeight(50)
        start_btn.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        start_btn.setStyleSheet(OnboardingScreenStyles.onboarding_button())
        start_btn.clicked.connect(self.start_onboarding)

        login_btn = QPushButton("Увійти з існуючим профілем")
        login_btn.setMinimumHeight(50)
        login_btn.setFont(QFont('Arial', 14))
        login_btn.setStyleSheet(OnboardingScreenStyles.welcome_login_button())
        login_btn.clicked.connect(self.login)

        button_layout.addWidget(start_btn)
        button_layout.addWidget(login_btn)
        button_layout.setSpacing(15)

        main_layout.addLayout(button_layout)

    def start_onboarding(self):
        self.parent.stack_widget.setCurrentIndex(1)

    def login(self):
        self.parent.stack_widget.setCurrentIndex(1)