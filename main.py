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
from views.onboarding.onboarding_manager import OnboardingManager

from controllers.data_controller import DataController
from utils.logger import get_logger

# Ініціалізація логування
logger = get_logger('main')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        logger.info("Запуск додатку 'Щоденник вагітності'")

        # Ініціалізуємо контролер даних
        self.data_controller = DataController()

        # Налаштування головного вікна
        self.init_ui()

    def init_ui(self):
        """Ініціалізація інтерфейсу користувача"""
        # Параметри вікна
        self.setWindowTitle("Щоденник вагітності")

        # Визначаємо розмір екрану (adaptive)
        screen_size = QApplication.primaryScreen().availableSize()
        window_width = min(420, screen_size.width() - 40)  # Збільшено до 420px або розмір екрану - 40px
        window_height = min(900, screen_size.height() - 60)  # Збільшено до 900px або розмір екрану - 60px

        # Встановлюємо розмір вікна з урахуванням екрану
        self.resize(window_width, window_height)

        # Головний віджет і layout
        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Стек для перемикання між екранами
        self.stack_widget = QStackedWidget()

        # Додаємо екран інформації про дитину як перший екран
        self.onboarding_manager = OnboardingManager(self)
        self.onboarding_manager.proceed_signal.connect(self.on_onboarding_completed)
        self.stack_widget.addWidget(self.onboarding_manager)

        # Завантажуємо основні екрани
        self.load_screens()

        # Додаємо стек до головного layout
        self.main_layout.addWidget(self.stack_widget, 1)

        # Створюємо нижню панель навігації
        self.create_bottom_nav()

        # Встановлюємо головний віджет
        self.setCentralWidget(main_widget)

        # Перевіряємо, чи це перший запуск додатку
        if self.data_controller.is_first_launch():
            logger.info("Виявлено перший запуск додатку. Показуємо екран введення даних дитини.")
            self.stack_widget.setCurrentIndex(0)  # Показуємо екран з інформацією про дитину
            self.hide_bottom_nav()  # Приховуємо нижню навігацію для екрану онбордингу
        else:
            logger.info("Не перший запуск. Показуємо основний екран.")
            self.stack_widget.setCurrentIndex(1)  # Показуємо екран тижнів

    def hide_bottom_nav(self):
        """Приховує нижню навігацію"""
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and item.widget() and item.widget() != self.stack_widget:
                item.widget().setVisible(False)
                logger.debug("Приховано елемент нижньої навігації")

    def show_bottom_nav(self):
        """Показує нижню навігацію"""
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if item and item.widget():
                item.widget().setVisible(True)
                logger.debug("Показано елемент нижньої навігації")

    def on_onboarding_completed(self, data):
        """Обробляє завершення введення всіх даних онбордингу"""
        logger.info("Отримана інформація про дитину та користувача, переходимо до основного екрану")

        # Зберігаємо дані
        success = self.data_controller.save_child_info(data)

        if success:
            # Показуємо нижню навігацію
            self.show_bottom_nav()

            # Переходимо до основного екрану
            self.stack_widget.setCurrentIndex(1)  # WeeksScreen
            logger.info("Успішно перейшли до основного екрану")
        else:
            # Повідомляємо про помилку
            QMessageBox.critical(self, "Помилка", "Не вдалося зберегти інформацію")
            logger.error("Не вдалося зберегти інформацію")

    def load_screens(self):
        logger.info("Завантаження екранів")

        try:
            # Додаємо екрани до стеку
            self.weeks_screen = WeeksScreen(self)
            self.calendar_screen = CalendarScreen(self)
            self.tools_screen = ToolsScreen(self)
            self.checklist_screen = ChecklistScreen(self)
            self.settings_screen = SettingsScreen(self)

            self.stack_widget.addWidget(self.weeks_screen)
            self.stack_widget.addWidget(self.calendar_screen)
            self.stack_widget.addWidget(self.tools_screen)
            self.stack_widget.addWidget(self.checklist_screen)
            self.stack_widget.addWidget(self.settings_screen)

            logger.info("Екрани успішно завантажені")

        except Exception as e:
            logger.error(f"Помилка завантаження екранів: {str(e)}")
            QMessageBox.critical(self, "Помилка", f"Помилка завантаження екранів: {str(e)}")

    def create_bottom_nav(self):
        # Створюємо панель навігації
        bottom_nav = QWidget()
        bottom_nav.setMinimumHeight(70)
        bottom_nav.setStyleSheet("background-color: #121212;")

        # Layout для кнопок
        nav_layout = QHBoxLayout(bottom_nav)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        nav_layout.setSpacing(2)  # Зменшуємо відстань між кнопками

        # Створюємо кнопки навігації
        nav_items = [
            {"icon": "resources/images/icons/weeks.png", "text": "Тижні", "index": 1},
            {"icon": "resources/images/icons/calendar.png", "text": "Календар", "index": 2},
            {"icon": "resources/images/icons/tools.png", "text": "Інструменти", "index": 3},
            {"icon": "resources/images/icons/checklist.png", "text": "Чекліст", "index": 4},
            {"icon": "resources/images/icons/settings.png", "text": "Налаштування", "index": 5}
        ]

        self.nav_buttons = []

        for item in nav_items:
            button = QPushButton()
            button.setObjectName(f"nav_{item['text'].lower()}")
            button.setCheckable(True)
            button.setFixedHeight(60)
            # Адаптивна ширина - встановлюємо мінімальну ширину, але дозволяємо розширюватись
            button.setMinimumWidth(65)
            button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

            # Встановлюємо іконку, якщо файл існує
            if os.path.exists(item["icon"]):
                button.setIcon(QIcon(item["icon"]))
                button.setIconSize(QSize(22, 22))

            # Встановлюємо текст і зменшуємо шрифт
            button.setText(item["text"])

            # Стиль для кнопок з меншим шрифтом
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #888888;
                    padding-top: 5px;
                    font-size: 9px;  /* Зменшений розмір шрифту */
                }
                QPushButton:checked {
                    color: #FF8C00;
                }
                QPushButton:hover {
                    color: #AAAAAA;
                }
            """)

            # Підключаємо подію кліку
            button.clicked.connect(lambda checked, idx=item["index"]: self.navigate_to(idx))

            nav_layout.addWidget(button)
            self.nav_buttons.append(button)

        # Додаємо панель навігації до головного layout
        self.main_layout.addWidget(bottom_nav)

    def navigate_to(self, screen_index):
        logger.info(f"Перехід на екран з індексом {screen_index}")
        self.stack_widget.setCurrentIndex(screen_index)

        # Оновлюємо вигляд кнопок навігації
        for i, button in enumerate(self.nav_buttons):
            # Враховуємо, що індекси екранів зміщені через додавання екрану онбордингу
            button.setChecked(i + 1 == screen_index)

        # Невелика візуальна анімація для показу зміни екрану
        QApplication.processEvents()

    def closeEvent(self, event):
        logger.info("Завершення роботи додатку")
        event.accept()


def setup_event_logging():
    # Клас для моніторингу подій PyQt
    original_notify = QApplication.notify

    def notify_wrapper(receiver, event):
        # Перехоплюємо події кліку на кнопки
        if event.type() == QEvent.Type.MouseButtonPress:
            try:
                if hasattr(receiver, 'text') and callable(receiver.text):
                    button_text = receiver.text()
                    if button_text:
                        logger.info(f"Клік на кнопку: {button_text}")
                elif hasattr(receiver, 'objectName') and receiver.objectName():
                    logger.info(f"Клік на об'єкт: {receiver.objectName()}")
                else:
                    # Для всіх інших віджетів логуємо тип об'єкта
                    logger.debug(f"Клік на {type(receiver).__name__}")
            except:
                pass  # Ігноруємо помилки під час логування

        # Передаємо подію оригінальному обробнику
        return original_notify(QApplication.instance(), receiver, event)

    # Правильна функція-обгортка для QApplication.notify
    def patched_notify(self, receiver, event):
        return notify_wrapper(receiver, event)

    # Підміняємо метод notify
    QApplication.notify = patched_notify


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Налаштування моніторингу подій
    setup_event_logging()

    # Застосовуємо темну тему
    app.setStyle("Fusion")

    # Завантаження та застосування стилів
    style_file = os.path.join("resources", "styles", "dark_theme.qss")
    try:
        with open(style_file, 'r') as f:
            style = f.read()
            app.setStyleSheet(style)
            logger.info("Стилі успішно застосовані")
    except Exception as e:
        logger.error(f"Помилка застосування стилів: {str(e)}")

    # Створюємо та запускаємо додаток
    window = MainWindow()
    window.show()

    sys.exit(app.exec())