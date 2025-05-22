import os
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QStackedWidget, QMessageBox, QSizePolicy)
from PyQt6.QtCore import QSize, QEvent
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
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Щоденник вагітності")

        screen_size = QApplication.primaryScreen().availableSize()
        window_width = min(390, screen_size.width() - 40)
        window_height = min(844, screen_size.height() - 60)
        self.resize(window_width, window_height)

        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.stack_widget = QStackedWidget()

        self.child_info_screen = ChildInfoScreen(self)
        self.child_info_screen.proceed_signal.connect(self.on_child_info_completed)
        self.stack_widget.addWidget(self.child_info_screen)

        self.user_info_screen = UserInfoScreen(self)
        self.user_info_screen.proceed_signal.connect(self.on_user_info_completed)
        logger.info("Сигнал UserInfoScreen підключено")
        self.stack_widget.addWidget(self.user_info_screen)

        self.load_screens()
        self.main_layout.addWidget(self.stack_widget, 1)
        self.create_bottom_nav()
        self.setCentralWidget(main_widget)

        if self.data_controller.is_first_launch():
            logger.info("Виявлено перший запуск додатку. Показуємо екран введення даних дитини.")
            self.stack_widget.setCurrentIndex(0)
            self.hide_bottom_nav()
        else:
            logger.info("Не перший запуск. Показуємо основний екран.")
            self.stack_widget.setCurrentIndex(2)

    def hide_bottom_nav(self):
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and item.widget() and item.widget() != self.stack_widget:
                item.widget().setVisible(False)
                logger.debug("Приховано елемент нижньої навігації")

    def show_bottom_nav(self):
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and item.widget():
                item.widget().setVisible(True)
                logger.debug("Показано елемент нижньої навігації")

    def on_child_info_completed(self, child_data):
        logger.info("Отримана інформація про дитину, переходимо до екрану інформації про користувача")
        success = self.data_controller.save_child_info(child_data)

        if success:
            self.stack_widget.setCurrentIndex(1)
            logger.info("Успішно перейшли до екрану інформації про користувача")
        else:
            QMessageBox.critical(self, "Помилка", "Не вдалося зберегти інформацію про дитину")
            logger.error("Не вдалося зберегти інформацію про дитину")

    def on_user_info_completed(self, user_data):
        logger.info(f"Отримана інформація про користувача: {user_data}")
        stack_index = self.stack_widget.indexOf(self.pregnancy_info_screen)
        if stack_index != -1:
            logger.info(f"Переходимо на екран інформації про вагітність (індекс {stack_index})")
            self.stack_widget.setCurrentIndex(stack_index)
        else:
            logger.error("Не вдалося знайти екран з інформацією про вагітність")
            self.stack_widget.setCurrentIndex(7)
        logger.info("Успішно перейшли до екрану інформації про вагітність")

    def on_pregnancy_info_completed(self, pregnancy_data):
        logger.info("Отримана інформація про вагітність, переходимо до основного екрану")
        try:
            last_period = datetime.strptime(pregnancy_data['last_period_date'], "%Y-%m-%d").date()
            self.data_controller.pregnancy_data.last_period_date = last_period

            conception = datetime.strptime(pregnancy_data['conception_date'], "%Y-%m-%d").date()
            self.data_controller.pregnancy_data.conception_date = conception

            self.data_controller.pregnancy_data.due_date = last_period + timedelta(days=280)
            self.data_controller.save_pregnancy_data()

            self.show_bottom_nav()
            self.stack_widget.setCurrentIndex(2)
            logger.info("Успішно перейшли до основного екрану")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти інформацію про вагітність: {str(e)}")
            logger.error(f"Не вдалося зберегти інформацію про вагітність: {str(e)}")

    def load_screens(self):
        logger.info("Завантаження екранів")
        try:
            self.weeks_screen = WeeksScreen(self)
            self.calendar_screen = CalendarScreen(self)
            self.tools_screen = ToolsScreen(self)
            self.checklist_screen = ChecklistScreen(self)
            self.settings_screen = SettingsScreen(self)
            self.pregnancy_info_screen = PregnancyInfoScreen(self)
            self.pregnancy_info_screen.proceed_signal.connect(self.on_pregnancy_info_completed)

            self.stack_widget.addWidget(self.weeks_screen)
            self.stack_widget.addWidget(self.calendar_screen)
            self.stack_widget.addWidget(self.tools_screen)
            self.stack_widget.addWidget(self.checklist_screen)
            self.stack_widget.addWidget(self.settings_screen)
            self.stack_widget.addWidget(self.pregnancy_info_screen)

            logger.info("Екрани успішно завантажені")
        except Exception as e:
            logger.error(f"Помилка завантаження екранів: {str(e)}")
            QMessageBox.critical(self, "Помилка", f"Помилка завантаження екранів: {str(e)}")

    def create_bottom_nav(self):
        bottom_nav = QWidget()
        bottom_nav.setObjectName("bottom_nav")
        bottom_nav.setMinimumHeight(70)
        bottom_nav.setStyleSheet(Styles.nav_bottom())

        nav_layout = QHBoxLayout(bottom_nav)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(2)

        nav_items = [
            {"icon": "resources/images/icons/weeks.png", "text": "Тижні", "index": 2},
            {"icon": "resources/images/icons/calendar.png", "text": "Календар", "index": 3},
            {"icon": "resources/images/icons/tools.png", "text": "Інструменти", "index": 4},
            {"icon": "resources/images/icons/checklist.png", "text": "Чекліст", "index": 5},
            {"icon": "resources/images/icons/settings.png", "text": "Налаштування", "index": 6}
        ]

        self.nav_buttons = []

        for item in nav_items:
            button = QPushButton()
            button.setObjectName(f"nav_{item['text'].lower()}")
            button.setCheckable(True)
            button.setFixedHeight(60)
            button.setMinimumWidth(60)
            button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

            if os.path.exists(item["icon"]):
                button.setIcon(QIcon(item["icon"]))
                button.setIconSize(QSize(22, 22))

            button.setText(item["text"])
            button.setStyleSheet(Styles.nav_button())
            button.clicked.connect(lambda checked, idx=item["index"]: self.navigate_to(idx))
            nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        self.main_layout.addWidget(bottom_nav)

    def navigate_to(self, screen_index):
        logger.info(f"Перехід на екран з індексом {screen_index}")
        self.stack_widget.setCurrentIndex(screen_index)

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i + 2 == screen_index)

        QApplication.processEvents()

    def closeEvent(self, event):
        logger.info("Завершення роботи додатку")
        event.accept()


def setup_event_logging():
    original_notify = QApplication.notify

    def notify_wrapper(receiver, event):
        if event.type() == QEvent.Type.MouseButtonPress:
            try:
                if hasattr(receiver, 'text') and callable(receiver.text):
                    button_text = receiver.text()
                    if button_text:
                        logger.info(f"Клік на кнопку: {button_text}")
                elif hasattr(receiver, 'objectName') and receiver.objectName():
                    logger.info(f"Клік на об'єкт: {receiver.objectName()}")
                else:
                    logger.debug(f"Клік на {type(receiver).__name__}")
            except:
                pass
        return original_notify(QApplication.instance(), receiver, event)

    def patched_notify(self, receiver, event):
        return notify_wrapper(receiver, event)

    QApplication.notify = patched_notify


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setup_event_logging()
    app.setStyle("Fusion")

    style_file = os.path.join("resources", "styles", "dark_theme.qss")
    try:
        with open(style_file, 'r') as f:
            style = f.read()
            app.setStyleSheet(style)
            logger.info("Стилі успішно застосовані")
    except Exception as e:
        logger.error(f"Помилка застосування стилів: {str(e)}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())