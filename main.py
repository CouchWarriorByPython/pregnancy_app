import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, \
    QMessageBox, QSizePolicy
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from views.weeks.weeks_screen import WeeksScreen
from views.calendar.calendar_screen import CalendarScreen
from views.tools.tools_screen import ToolsScreen
from views.checklist.checklist_screen import ChecklistScreen
from views.settings.settings_screen import SettingsScreen
from views.onboarding.child_info_screen import ChildInfoScreen
from views.onboarding.user_info_screen import UserInfoScreen
from views.onboarding.pregnancy_info_screen import PregnancyInfoScreen

from controllers.data_controller import DataController
from utils.logger import get_logger
from utils.styles import Styles
from datetime import datetime, timedelta

logger = get_logger('main')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("Запуск додатку 'Щоденник вагітності'")
        self.data_controller = DataController()
        self._setup_window()
        self._create_screens()
        self._setup_navigation()
        self._setup_layout()
        self._handle_first_launch()

    def _setup_window(self):
        self.setWindowTitle("Щоденник вагітності")
        screen_size = QApplication.primaryScreen().availableSize()
        self.resize(min(390, screen_size.width() - 40), min(844, screen_size.height() - 60))

    def _create_screens(self):
        self.stack_widget = QStackedWidget()

        self.screens = {
            'child_info': ChildInfoScreen(self),
            'user_info': UserInfoScreen(self),
            'weeks': WeeksScreen(self),
            'calendar': CalendarScreen(self),
            'tools': ToolsScreen(self),
            'checklist': ChecklistScreen(self),
            'settings': SettingsScreen(self),
            'pregnancy_info': PregnancyInfoScreen(self)
        }

        for screen in self.screens.values():
            self.stack_widget.addWidget(screen)

        self.screens['child_info'].proceed_signal.connect(self.on_child_info_completed)
        self.screens['user_info'].proceed_signal.connect(self.on_user_info_completed)
        self.screens['pregnancy_info'].proceed_signal.connect(self.on_pregnancy_info_completed)

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

    def _handle_first_launch(self):
        if self.data_controller.is_first_launch():
            logger.info("Виявлено перший запуск додатку. Показуємо екран введення даних дитини.")
            self.stack_widget.setCurrentWidget(self.screens['child_info'])
            self.bottom_nav.setVisible(False)
        else:
            logger.info("Не перший запуск. Показуємо основний екран.")
            self.stack_widget.setCurrentWidget(self.screens['weeks'])

    def navigate_to(self, screen_name):
        logger.info(f"Перехід на екран: {screen_name}")
        self.stack_widget.setCurrentWidget(self.screens[screen_name])

        screen_indices = list(self.screens.keys())
        main_screens = ['weeks', 'calendar', 'tools', 'checklist', 'settings']

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(main_screens[i] == screen_name)

    def on_child_info_completed(self, child_data):
        logger.info("Отримана інформація про дитину, переходимо до екрану інформації про користувача")
        if self.data_controller.save_child_info(child_data):
            self.stack_widget.setCurrentWidget(self.screens['user_info'])
        else:
            QMessageBox.critical(self, "Помилка", "Не вдалося зберегти інформацію про дитину")

    def on_user_info_completed(self, user_data):
        logger.info(f"Отримана інформація про користувача: {user_data}")
        self.stack_widget.setCurrentWidget(self.screens['pregnancy_info'])

    def on_pregnancy_info_completed(self, pregnancy_data):
        logger.info("Отримана інформація про вагітність, переходимо до основного екрану")
        try:
            last_period = datetime.strptime(pregnancy_data['last_period_date'], "%Y-%m-%d").date()
            conception = datetime.strptime(pregnancy_data['conception_date'], "%Y-%m-%d").date()

            self.data_controller.pregnancy_data.last_period_date = last_period
            self.data_controller.pregnancy_data.conception_date = conception
            self.data_controller.pregnancy_data.due_date = last_period + timedelta(days=280)
            self.data_controller.save_pregnancy_data()

            self.bottom_nav.setVisible(True)
            self.stack_widget.setCurrentWidget(self.screens['weeks'])
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти інформацію про вагітність: {str(e)}")

    def closeEvent(self, event):
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