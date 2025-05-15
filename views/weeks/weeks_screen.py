from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QHBoxLayout,
                             QSizePolicy, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from controllers.data_controller import DataController
from controllers.baby_development_controller import BabyDevelopmentController
from .fruit_comparison_view import FruitComparisonView
from utils.logger import get_logger
from utils.image_utils import generate_circle_image

logger = get_logger('weeks_screen')


class InfoCard(QFrame):
    """Інформаційна картка для екрану тижнів"""

    def __init__(self, title, content, icon_path=None, parent=None):
        super().__init__(parent)

        # Ініціалізуємо атрибути заздалегідь
        self.title_label = None
        self.content_label = None
        self.is_hover = False

        self.setup_ui(title, content, icon_path)

        # Додаємо відстеження подій миші для інтерактивності
        self.setMouseTracking(True)

    def setup_ui(self, title, content, icon_path):
        # Стиль для карток
        self.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)

        # Головний layout
        card_layout = QVBoxLayout(self)

        # Заголовок з іконкою
        header_layout = QHBoxLayout()

        # Іконка (замінена на коло, якщо файл не знайдено)
        icon_label = QLabel()
        icon_found = False

        if icon_path:
            try:
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    icon_label.setPixmap(pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio))
                    header_layout.addWidget(icon_label)
                    icon_found = True
            except Exception as e:
                logger.error(f"Помилка завантаження іконки: {e}")

        # Якщо іконка не знайдена, використовуємо коло
        if not icon_found:
            circle_pixmap = generate_circle_image(size=24, color="#FF8C00")
            icon_label.setPixmap(circle_pixmap)
            header_layout.addWidget(icon_label)

        # Заголовок
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        # Додаємо заголовок до головного layout
        card_layout.addLayout(header_layout)

        # Вміст
        self.content_label = QLabel(content)
        self.content_label.setWordWrap(True)
        self.content_label.setFont(QFont('Arial', 12))
        self.content_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card_layout.addWidget(self.content_label)

        # Встановлюємо розміри картки
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    # Обробники подій миші для інтерактивності
    def enterEvent(self, event):
        self.is_hover = True
        self.setStyleSheet("""
            QFrame {
                background-color: #2A2A2A;
                border-radius: 15px;
                padding: 10px;
                border: 1px solid #FF8C00;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hover = False
        self.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
                border: none;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet("""
                QFrame {
                    background-color: #333333;
                    border-radius: 15px;
                    padding: 10px;
                    border: 1px solid #FF8C00;
                }
                QLabel {
                    color: #FFFFFF;
                }
            """)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_hover:
                self.setStyleSheet("""
                    QFrame {
                        background-color: #2A2A2A;
                        border-radius: 15px;
                        padding: 10px;
                        border: 1px solid #FF8C00;
                    }
                    QLabel {
                        color: #FFFFFF;
                    }
                """)
            else:
                self.setStyleSheet("""
                    QFrame {
                        background-color: #222222;
                        border-radius: 15px;
                        padding: 10px;
                        border: none;
                    }
                    QLabel {
                        color: #FFFFFF;
                    }
                """)
        super().mouseReleaseEvent(event)


class WeeksScreen(QWidget):
    """Екран з інформацією про тижні вагітності"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # Ініціалізуємо атрибути заздалегідь
        self.content_layout = None
        self.cards_layout = None
        self.cards_section = None
        self.week_selector = None
        self.baby_info_section = None
        self.fruit_comparison_view = None
        self.current_displayed_week = None
        self.week_btns = []
        self.prev_btn = None
        self.next_btn = None
        self.week_title = None

        logger.info("Ініціалізація екрану тижнів вагітності")

        self.data_controller = DataController()
        self.baby_dev_controller = BabyDevelopmentController()

        self.current_week = self.data_controller.get_current_week() or 33
        self.available_weeks = self.baby_dev_controller.get_available_weeks()

        logger.info(f"Поточний тиждень вагітності: {self.current_week}")

        self.setup_ui()

    def lighten_color(self, hex_color, factor=0.2):
        """Освітлює RGB колір на заданий фактор"""
        # Конвертуємо hex в RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        # Освітлюємо кожен компонент
        r = min(int(r + (255 - r) * factor), 255)
        g = min(int(g + (255 - g) * factor), 255)
        b = min(int(b + (255 - b) * factor), 255)

        # Конвертуємо назад у hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_week_color(self, week):
        """Повертає колір для тижня відповідно до триместру"""
        if week <= 13:  # Перший триместр
            return "#E91E63"  # Рожевий
        elif week <= 27:  # Другий триместр
            return "#9C27B0"  # Фіолетовий
        else:  # Третій триместр
            return "#3F51B5"  # Синій

    def create_week_button(self, week, is_current=False):
        """Створює кнопку для тижня з відповідними стилями"""
        color = self.get_week_color(week)

        week_btn = QPushButton(str(week))
        week_btn.setObjectName(f"week_btn_{week}")
        week_btn.setFixedSize(60, 60)
        week_btn.setCheckable(True)
        week_btn.setChecked(is_current)

        # Стиль для круглої кнопки
        week_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 30px;
                font-weight: bold;
                font-size: 18px;
                color: white;
                text-align: center;
            }}
            QPushButton:checked {{
                background-color: #FF8C00;
                color: white;
            }}
            QPushButton:hover:!checked {{
                background-color: {self.lighten_color(color)};
            }}
        """)

        # Зберігаємо тиждень як властивість кнопки
        week_btn.week = week

        # Підключаємо сигнал
        week_btn.clicked.connect(lambda checked, b=week_btn: self.week_changed(b.week))

        return week_btn

    def setup_ui(self):
        """Налаштування інтерфейсу користувача"""
        # Головний вертикальний layout для всього екрану
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Розділ з кнопками вибору тижня (верхня частина екрану)
        week_selector_section = QWidget()
        week_selector_section.setObjectName("week_selector_section")
        week_selector_section.setMaximumHeight(100)

        week_selector_layout = QHBoxLayout(week_selector_section)
        week_selector_layout.setContentsMargins(10, 10, 10, 10)

        # Кнопка "назад"
        self.prev_btn = QPushButton("<")
        self.prev_btn.setObjectName("prev_week_btn")
        self.prev_btn.setFixedSize(45, 45)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border-radius: 22px;
                font-weight: bold;
                color: #DDDDDD;
                font-size: 18px;
            }
            QPushButton:disabled {
                background-color: #222222;
                color: #555555;
            }
            QPushButton:hover:enabled {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_week)
        week_selector_layout.addWidget(self.prev_btn)

        # Знаходимо індекс поточного тижня серед доступних
        current_index = self.get_current_week_index()

        # Визначаємо діапазон тижнів для показу
        visible_weeks = self.get_visible_weeks_range(current_index)

        # Створюємо кнопки тижнів
        self.week_btns = []
        for week in visible_weeks:
            week_btn = self.create_week_button(week, week == self.current_week)
            week_selector_layout.addWidget(week_btn)
            self.week_btns.append(week_btn)

        # Кнопка "вперед"
        self.next_btn = QPushButton(">")
        self.next_btn.setObjectName("next_week_btn")
        self.next_btn.setFixedSize(45, 45)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border-radius: 22px;
                font-weight: bold;
                color: #DDDDDD;
                font-size: 18px;
            }
            QPushButton:disabled {
                background-color: #222222;
                color: #555555;
            }
            QPushButton:hover:enabled {
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
        """)
        self.next_btn.clicked.connect(self.next_week)
        week_selector_layout.addWidget(self.next_btn)

        # Додаємо вибір тижня до головного layout
        main_layout.addWidget(week_selector_section)

        # Створюємо скролований контейнер для основного контенту
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        # Основний контент
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        # Заголовок з номером тижня
        self.week_title = QLabel(f"Тиждень {self.current_week}")
        self.week_title.setObjectName("week_title_label")
        self.week_title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        self.week_title.setStyleSheet("color: #FF8C00;")
        self.week_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.week_title)

        # Віджет для порівняння з фруктами (створюємо заглушку, буде оновлено в update_content)
        self.fruit_comparison_view = None

        # Секція з картками інформації
        cards_section = QWidget()
        self.cards_layout = QVBoxLayout(cards_section)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)

        # Додаємо секцію з картками до контенту
        self.content_layout.addWidget(cards_section)

        # Додаємо контент до області прокрутки
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        # Оновлюємо стан кнопок
        self.update_buttons_state()

        # Оновлюємо контент для поточного тижня
        self.update_content(self.current_week)

    def get_current_week_index(self):
        """Знаходить індекс поточного тижня серед доступних"""
        if self.current_week in self.available_weeks:
            return self.available_weeks.index(self.current_week)

        # Якщо поточний тиждень не знайдено, вибираємо найближчий
        current_index = 0
        min_diff = abs(self.available_weeks[0] - self.current_week)

        for i, week in enumerate(self.available_weeks):
            diff = abs(week - self.current_week)
            if diff < min_diff:
                min_diff = diff
                current_index = i

        self.current_week = self.available_weeks[current_index]
        logger.info(f"Тиждень {self.current_week} не знайдено серед доступних. "
                    f"Встановлено найближчий: {self.current_week}")

        return current_index

    def get_visible_weeks_range(self, current_index):
        """Розраховує діапазон видимих тижнів"""
        total_buttons = 5
        half_range = total_buttons // 2

        # Розраховуємо початковий і кінцевий індекси
        start_idx = max(0, current_index - half_range)
        end_idx = min(len(self.available_weeks), start_idx + total_buttons)

        # Якщо не вистачає тижнів з правого боку, додаємо більше з лівого
        if end_idx - start_idx < total_buttons and start_idx > 0:
            shift = total_buttons - (end_idx - start_idx)
            start_idx = max(0, start_idx - shift)

        return self.available_weeks[start_idx:end_idx]

    def update_ui_for_week(self, week):
        """Оновлює інтерфейс для показу нового діапазону тижнів"""
        logger.info(f"Оновлення UI тижнів для тижня {week}")

        # Очищаємо поточні кнопки
        for btn in self.week_btns:
            btn.deleteLater()
        self.week_btns.clear()

        # Отримуємо layout, де знаходяться кнопки
        week_selector_layout = None
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget and widget.objectName() == "week_selector_section":
                week_selector_layout = widget.layout()
                break

        if not week_selector_layout:
            logger.error("Не знайдено layout селектора тижнів")
            return

        # Видаляємо всі елементи крім першого (prev_btn) і останнього (next_btn)
        for i in reversed(range(1, week_selector_layout.count() - 1)):
            item = week_selector_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                week_selector_layout.removeItem(item)

        # Знаходимо індекс поточного тижня
        if week in self.available_weeks:
            current_index = self.available_weeks.index(week)
        else:
            # Якщо тиждень не знайдено, шукаємо найближчий
            current_index = 0
            min_diff = abs(self.available_weeks[0] - week)
            for i, w in enumerate(self.available_weeks):
                diff = abs(w - week)
                if diff < min_diff:
                    min_diff = diff
                    current_index = i
            week = self.available_weeks[current_index]

        self.current_week = week

        # Отримуємо видимий діапазон тижнів
        visible_weeks = self.get_visible_weeks_range(current_index)

        # Створюємо нові кнопки
        for i, week in enumerate(visible_weeks):
            week_btn = self.create_week_button(week, week == self.current_week)
            # Вставляємо кнопку перед кнопкою "вперед"
            week_selector_layout.insertWidget(i + 1, week_btn)
            self.week_btns.append(week_btn)

        # Оновлюємо стан кнопок
        self.update_buttons_state()

    def update_content(self, week):
        """Оновлює контент відповідно до вибраного тижня"""
        logger.info(f"Оновлення контенту для тижня {week}")

        if hasattr(self, 'week_title'):
            self.week_title.setText(f"Тиждень {week}")

        # Перевіряємо, чи змінився тиждень
        if self.current_displayed_week == week:
            logger.info(f"Тиждень {week} вже відображається, пропускаємо оновлення")
            return

        self.current_displayed_week = week

        # Очищаємо поточні картки
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Отримуємо дані про розвиток дитини
        # Використовуємо стать дитини для персоналізації інформації
        child_info = self.data_controller.get_child_info()

        baby_dev_info = self.baby_dev_controller.get_baby_development_info(week, gender=child_info["gender"])
        mother_changes = self.baby_dev_controller.get_mother_changes_info(week)
        nutrition_tips = self.baby_dev_controller.get_nutrition_tips(week)

        fruit_data = self.baby_dev_controller.get_fruit_comparison(week)
        size_data = self.baby_dev_controller.get_baby_size(week)

        logger.info(f"Завантажено дані про тиждень {week}: розмір дитини - {size_data['length']}")

        if fruit_data:
            fruit_data.update(size_data)
            if self.fruit_comparison_view:
                self.fruit_comparison_view.update_fruit_data(week, fruit_data)
                logger.info(f"Оновлено порівняння з фруктом: {fruit_data['fruit']}")
            else:
                self.fruit_comparison_view = FruitComparisonView(week, fruit_data)
                self.content_layout.insertWidget(1, self.fruit_comparison_view)
                logger.info(f"Створено нове порівняння з фруктом: {fruit_data['fruit']}")

        # Додаємо нові картки
        cards_data = [
            {
                "title": "Зростання вашої дитини",
                "content": baby_dev_info,
                "icon": "resources/images/icons/development.png"
            },
            {
                "title": "Все про вас",
                "content": mother_changes,
                "icon": "resources/images/icons/symptoms.png"
            },
            {
                "title": "Поради щодо харчування",
                "content": nutrition_tips,
                "icon": "resources/images/icons/nutrition.png"
            },
            {
                "title": "Поради для вашого терміну",
                "content": "На цьому тижні важливо слідкувати за своїм здоров'ям та відвідувати лікаря за розкладом.",
                "icon": "resources/images/icons/tips.png"
            }
        ]

        for card_data in cards_data:
            logger.debug(f"Створення картки: {card_data['title']}")
            card = InfoCard(
                title=card_data["title"],
                content=card_data["content"],
                icon_path=card_data.get("icon"),
                parent=self
            )
            self.cards_layout.addWidget(card)

        logger.info(f"Контент для тижня {week} успішно оновлено")

    def week_changed(self, week):
        """Обробка зміни тижня"""
        if week != self.current_week:
            logger.info(f"Зміна тижня: з {self.current_week} на {week}")

            # Зберігаємо новий поточний тиждень
            old_week = self.current_week
            self.current_week = week

            # Оновлюємо стан кнопок
            self.update_buttons_state()

            # Оновлюємо контент
            self.update_content(week)

    def update_buttons_state(self):
        """Оновлення стану кнопок тижнів"""
        # Оновлюємо стан кнопок тижнів
        for btn in self.week_btns:
            btn.setChecked(btn.week == self.current_week)

        # Знаходимо індекс поточного тижня для визначення стану кнопок навігації
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)

            # Кнопка "назад" активна, якщо є попередні тижні
            self.prev_btn.setEnabled(current_index > 0)

            # Кнопка "вперед" активна, якщо є наступні тижні
            self.next_btn.setEnabled(current_index < len(self.available_weeks) - 1)
        else:
            # Якщо тиждень не знайдено, вимикаємо обидві кнопки
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            logger.warning(f"Тиждень {self.current_week} не знайдено серед доступних")

    def prev_week(self):
        """Перехід до попереднього тижня"""
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            if current_index > 0:
                new_week = self.available_weeks[current_index - 1]
                logger.info(f"Перехід до попереднього тижня: {new_week}")

                # Перевіряємо, чи новий тиждень є серед видимих кнопок або на краю діапазону
                visible_weeks = [btn.week for btn in self.week_btns]
                if new_week not in visible_weeks or new_week == min(visible_weeks):
                    self.update_ui_for_week(new_week)

                # Потім змінюємо тиждень і оновлюємо контент
                self.week_changed(new_week)

    def next_week(self):
        """Перехід до наступного тижня"""
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            if current_index < len(self.available_weeks) - 1:
                new_week = self.available_weeks[current_index + 1]
                logger.info(f"Перехід до наступного тижня: {new_week}")

                # Перевіряємо, чи новий тиждень є серед видимих кнопок або на краю діапазону
                visible_weeks = [btn.week for btn in self.week_btns]
                if new_week not in visible_weeks or new_week == max(visible_weeks):
                    self.update_ui_for_week(new_week)

                # Потім змінюємо тиждень і оновлюємо контент
                self.week_changed(new_week)