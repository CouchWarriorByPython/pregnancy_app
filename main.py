import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, \
    QMessageBox, QSizePolicy
from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QIcon

from views.weeks.weeks_screen import WeeksScreen
from views.calendar.calendar_screen import CalendarScreen
from views.tools.tools_screen import ToolsScreen
from views.checklist.checklist_screen import ChecklistScreen
from views.settings.settings_screen import SettingsScreen
from views.onboarding.child_info_screen import ChildInfoScreen
from views.onboarding.user_info_screen import UserInfoScreen
from views.onboarding.pregnancy_info_screen import PregnancyInfoScreen
from views.auth.login_screen import LoginScreen
from views.auth.register_screen import RegisterScreen
from views.auth.verification_screen import VerificationScreen

from controllers.data_controller import DataController
from controllers.auth_controller import AuthController
from utils.logger import get_logger
from utils.styles import Styles
from utils.reminder_service import ReminderService
from datetime import datetime, timedelta

logger = get_logger('main')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Запуск додатку 'Щоденник вагітності'")
        self.current_user_id = None
        self.current_user_email = None
        self.data_controller = None
        self.auth_controller = AuthController()
        self.reminder_service = None
        self._setup_window()
        self._create_screens()
        self._setup_navigation()
        self._setup_layout()
        self._handle_authentication()

    def _setup_window(self):
        self.setWindowTitle("Щоденник вагітності")
        screen_size = QApplication.primaryScreen().availableSize()
        self.resize(min(390, screen_size.width() - 40), min(844, screen_size.height() - 60))

    def _create_screens(self):
        self.stack_widget = QStackedWidget()

        self.auth_screens = {
            'login': LoginScreen(self),
            'register': RegisterScreen(self),
            'verification': VerificationScreen(parent=self)
        }

        # Створюємо головні екрани без DataController
        self.main_screens = {
            'child_info': ChildInfoScreen(self),
            'user_info': UserInfoScreen(self),
            'weeks': WeeksScreen(self),
            'calendar': CalendarScreen(self),
            'tools': ToolsScreen(self),
            'checklist': ChecklistScreen(self),
            'settings': SettingsScreen(self),
            'pregnancy_info': PregnancyInfoScreen(self)
        }

        all_screens = {**self.auth_screens, **self.main_screens}
        for screen in all_screens.values():
            self.stack_widget.addWidget(screen)

        self._connect_auth_signals()
        self._connect_onboarding_signals()

    def _connect_auth_signals(self):
        self.auth_screens['login'].login_success.connect(self.on_login_success)
        self.auth_screens['login'].switch_to_register.connect(lambda: self.show_screen('register'))

        self.auth_screens['register'].registration_success.connect(self.on_registration_success)
        self.auth_screens['register'].switch_to_login.connect(lambda: self.show_screen('login'))

        self.auth_screens['verification'].verification_success.connect(self.on_verification_success)
        self.auth_screens['verification'].back_to_register.connect(lambda: self.show_screen('register'))

    def _connect_onboarding_signals(self):
        self.main_screens['child_info'].proceed_signal.connect(self.on_child_info_completed)
        self.main_screens['user_info'].proceed_signal.connect(self.on_user_info_completed)
        self.main_screens['pregnancy_info'].proceed_signal.connect(self.on_pregnancy_info_completed)

    def _setup_navigation(self):
        nav_items = [
            {"icon": "resources/images/icons/weeks.png", "text": "Тижні", "screen": "weeks"},
            {"icon": "resources/images/icons/calendar.png", "text": "Календар", "screen": "calendar"},
            {"icon": "resources/images/icons/tools.png", "text": "Інструменти", "screen": "tools"},
            {"icon": "resources/images/icons/checklist.png", "text": "Чекліст", "screen": "checklist"},
            {"icon": "resources/images/icons/settings.png", "text": "Налаштування", "screen": "settings"}
        ]

        self.nav_buttons = []
        self.bottom_nav = QWidget()
        self.bottom_nav.setMinimumHeight(70)
        self.bottom_nav.setStyleSheet(Styles.nav_bottom())

        nav_layout = QHBoxLayout(self.bottom_nav)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(2)

        for item in nav_items:
            button = self._create_nav_button(item)
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)

    def _create_nav_button(self, item):
        button = QPushButton()
        button.setCheckable(True)
        button.setFixedHeight(60)
        button.setMinimumWidth(60)
        button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        if os.path.exists(item["icon"]):
            button.setIcon(QIcon(item["icon"]))
            button.setIconSize(QSize(22, 22))

        button.setText(item["text"])
        button.setStyleSheet(Styles.nav_button())
        button.clicked.connect(lambda: self.navigate_to(item["screen"]))
        return button

    def _setup_layout(self):
        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.stack_widget, 1)
        self.main_layout.addWidget(self.bottom_nav)
        self.setCentralWidget(main_widget)

    def _handle_authentication(self):
        self.bottom_nav.setVisible(False)
        self.show_screen('login')

    def show_screen(self, screen_name):
        if screen_name in self.auth_screens:
            screen = self.auth_screens[screen_name]
        else:
            screen = self.main_screens[screen_name]
        self.stack_widget.setCurrentWidget(screen)

    def on_login_success(self, user_data):
        logger.info(f"Успішний вхід користувача {user_data['email']}")
        self.current_user_id = user_data['user_id']
        self.current_user_email = user_data['email']
        self.data_controller = DataController(self.current_user_id)
        self._init_reminder_service()

        if self.data_controller.is_first_launch():
            logger.info("Перший запуск для користувача. Показуємо онбординг.")
            self.show_screen('child_info')
            self.bottom_nav.setVisible(False)
        else:
            logger.info("Користувач авторизований. Показуємо головний екран.")
            self._update_screens_with_user_data()
            self.bottom_nav.setVisible(True)
            self.show_screen('weeks')

    def on_registration_success(self, email):
        logger.info(f"Успішна реєстрація користувача {email}")
        verification_screen = self.auth_screens['verification']
        verification_screen.set_email(email)
        self.show_screen('verification')

    def on_verification_success(self, user_data):
        logger.info(f"Успішне підтвердження пошти {user_data['email']}")
        self.current_user_id = user_data['user_id']
        self.current_user_email = user_data['email']
        self.data_controller = DataController(self.current_user_id)
        self._init_reminder_service()
        self.show_screen('child_info')
        self.bottom_nav.setVisible(False)

    def _init_reminder_service(self):
        if self.data_controller:
            self.reminder_service = ReminderService(
                self.data_controller.db,
                self.current_user_id,
                self.current_user_email  # Додаємо email
            )
            self.reminder_service.start()

    def _update_screens_with_user_data(self):
        """Оновлюємо екрани з правильним DataController після авторизації"""
        for screen_name, screen in self.main_screens.items():
            if hasattr(screen, 'data_controller'):
                screen.data_controller = DataController(self.current_user_id)
            if hasattr(screen, 'parent'):
                screen.parent = self

    def navigate_to(self, screen_name):
        logger.info(f"Перехід на екран: {screen_name}")
        self.show_screen(screen_name)

        screen_indices = list(self.main_screens.keys())
        main_screens = ['weeks', 'calendar', 'tools', 'checklist', 'settings']

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(main_screens[i] == screen_name)

    def on_child_info_completed(self, child_data):
        logger.info("Отримана інформація про дитину, переходимо до екрану інформації про користувача")
        if self.data_controller and self.data_controller.save_child_info(child_data):
            self.show_screen('user_info')
        else:
            QMessageBox.critical(self, "Помилка", "Не вдалося зберегти інформацію про дитину")

    def on_user_info_completed(self, user_data):
        logger.info(f"Отримана інформація про користувача: {user_data}")
        self.show_screen('pregnancy_info')

    def on_pregnancy_info_completed(self, pregnancy_data):
        logger.info("Отримана інформація про вагітність, переходимо до основного екрану")
        try:
            last_period = datetime.strptime(pregnancy_data['last_period_date'], "%Y-%m-%d").date()
            conception = datetime.strptime(pregnancy_data['conception_date'], "%Y-%m-%d").date()

            if last_period > conception:
                QMessageBox.warning(self, "Помилка", "Дата останньої менструації не може бути пізніше дати зачаття")
                return

            if self.data_controller:
                self.data_controller.pregnancy_data.last_period_date = last_period
                self.data_controller.pregnancy_data.conception_date = conception
                self.data_controller.save_pregnancy_data()

                self._update_screens_with_user_data()
                self.bottom_nav.setVisible(True)
                self.show_screen('weeks')
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти інформацію про вагітність: {str(e)}")

    def logout(self):
        self.auth_controller.logout()
        self.current_user_id = None
        self.current_user_email = None
        self.data_controller = None
        if self.reminder_service:
            self.reminder_service.stop()
            self.reminder_service = None

        self.bottom_nav.setVisible(False)
        self.show_screen('login')
        logger.info("Користувач вийшов з системи")

    def closeEvent(self, event):
        if self.reminder_service:
            self.reminder_service.stop()
        logger.info("Завершення роботи додатку")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    style_file = os.path.join("resources", "styles", "dark_theme.qss")
    try:
        with open(style_file, 'r') as f:
            app.setStyleSheet(f.read())
            logger.info("Стилі успішно застосовані")
    except Exception as e:
        logger.error(f"Помилка застосування стилів: {str(e)}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())