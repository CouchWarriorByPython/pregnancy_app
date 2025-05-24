from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import pyqtSignal
from utils.logger import get_logger
from .child_info_screen import ChildInfoScreen
from .user_info_screen import UserInfoScreen

logger = get_logger('onboarding_manager')


class OnboardingManager(QWidget):
    """Менеджер екранів онбордингу, який керує послідовністю екранів"""

    proceed_signal = pyqtSignal(dict)  # Сигнал для переходу далі з даними

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.child_data = {}
        self.user_data = {}

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Стек для перемикання між екранами
        self.stack = QStackedWidget()

        # Екран інформації про дитину
        self.child_info_screen = ChildInfoScreen(self)
        self.child_info_screen.proceed_signal.connect(self.on_child_info_completed)

        # Екран інформації про користувача
        self.user_info_screen = UserInfoScreen(self)
        self.user_info_screen.proceed_signal.connect(self.on_user_info_completed)

        # Додаємо екрани до стеку
        self.stack.addWidget(self.child_info_screen)
        self.stack.addWidget(self.user_info_screen)

        layout.addWidget(self.stack)

    def on_child_info_completed(self, data):
        """Обробка завершення введення інформації про дитину"""
        logger.info(f"Отримана інформація про дитину: {data}")
        self.child_data = data

        # Переходимо до наступного екрану
        self.stack.setCurrentIndex(1)

    def on_user_info_completed(self, data):
        """Обробка завершення введення інформації про користувача"""
        logger.info(f"Отримана інформація про користувача: {data}")
        self.user_data = data

        # Об'єднуємо дані
        complete_data = self.child_data.copy()
        complete_data["user_data"] = self.user_data

        # Відправляємо сигнал із повними даними
        self.proceed_signal.emit(complete_data)