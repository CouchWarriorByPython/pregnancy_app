from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QHBoxLayout,
                             QSizePolicy, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
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


class WeekSelector(QWidget):
    """Віджет для вибору тижня вагітності"""

    # Сигнал для сповіщення про зміну тижня
    week_changed_signal = pyqtSignal(int)

    def __init__(self, current_week, available_weeks, on_week_change, parent=None):
        super().__init__(parent)

        # Зберігаємо початкові дані
        self.current_week = current_week
        self.available_weeks = available_weeks
        self.on_week_change = on_week_change

        # Ініціалізуємо атрибути
        self.prev_btn = None
        self.next_btn = None
        self.week_btns = []

        # Налаштовуємо інтерфейс
        self.setup_ui()

    def setup_ui(self):
        """Налаштування інтерфейсу користувача"""
        # Головний горизонтальний layout без відступів
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Кнопка "назад"
        self.prev_btn = QPushButton("<")
        self.prev_btn.setObjectName("prev_week_btn")
        self.prev_btn.setFixedSize(40, 40)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border-radius: 20px;
                font-weight: bold;
                color: #DDDDDD;
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
        layout.addWidget(self.prev_btn)

        # ДИНАМІЧНЕ СТВОРЕННЯ КНОПОК ТИЖНІВ
        self.week_btns = []

        # Знаходимо індекс поточного тижня серед доступних
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
        else:
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

        # Визначаємо діапазон тижнів для показу (завжди 5 кнопок)
        total_buttons = 5
        half_range = total_buttons // 2

        # Розраховуємо початковий і кінцевий індекси
        start_idx = max(0, current_index - half_range)
        end_idx = min(len(self.available_weeks), start_idx + total_buttons)

        # Якщо не вистачає тижнів з правого боку, додаємо більше з лівого
        if end_idx - start_idx < total_buttons and start_idx > 0:
            shift = total_buttons - (end_idx - start_idx)
            start_idx = max(0, start_idx - shift)

        # Отримуємо тижні для показу
        visible_weeks = self.available_weeks[start_idx:end_idx]

        logger.debug(f"Видимі тижні: {visible_weeks}, поточний: {self.current_week}")

        # Створюємо кнопки для кожного тижня з кольоровим фоном та цифрами, як на зображенні 5
        for week in visible_weeks:
            # Встановлюємо колір фону залежно від тижня
            color = self.get_week_color(week)

            week_btn = QPushButton(str(week))
            week_btn.setObjectName(f"week_btn_{week}")
            week_btn.setFixedSize(60, 60)
            week_btn.setCheckable(True)
            week_btn.setChecked(week == self.current_week)

            # Встановлюємо стиль з кольоровим фоном
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
            """)

            # Зберігаємо тиждень як властивість кнопки
            week_btn.week = week

            # Створюємо локальну копію для замикання
            current_btn = week_btn
            current_btn.clicked.connect(lambda checked, b=current_btn: self.week_changed(b.week))

            layout.addWidget(week_btn)
            self.week_btns.append(week_btn)

        # Кнопка "вперед"
        self.next_btn = QPushButton(">")
        self.next_btn.setObjectName("next_week_btn")
        self.next_btn.setFixedSize(40, 40)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                border-radius: 20px;
                font-weight: bold;
                color: #DDDDDD;
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
        layout.addWidget(self.next_btn)

        # Оновлюємо стан кнопок
        self.update_buttons_state()

        # Налаштування розміру віджета
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def get_week_color(self, week):
        """Повертає колір для тижня відповідно до триместру"""
        if week <= 13:  # Перший триместр
            return "#E91E63"  # Рожевий
        elif week <= 27:  # Другий триместр
            return "#9C27B0"  # Фіолетовий
        else:  # Третій триместр
            return "#3F51B5"  # Синій

    def update_ui_for_week(self, week):
        """Оновлює інтерфейс для показу нового діапазону тижнів"""
        logger.info(f"Оновлення UI селектора для тижня {week}")

        # Очищаємо поточні кнопки
        for btn in self.week_btns:
            btn.deleteLater()
        self.week_btns.clear()

        # Створюємо новий layout
        layout = self.layout()

        # Видаляємо всі елементи крім першого (prev_btn) і останнього (next_btn)
        for i in reversed(range(1, layout.count() - 1)):
            item = layout.itemAt(i)
            if item and item.widget():
                layout.removeItem(item)

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

        # Визначаємо діапазон тижнів для показу
        total_buttons = 5
        half_range = total_buttons // 2

        start_idx = max(0, current_index - half_range)
        end_idx = min(len(self.available_weeks), start_idx + total_buttons)

        if end_idx - start_idx < total_buttons and start_idx > 0:
            shift = total_buttons - (end_idx - start_idx)
            start_idx = max(0, start_idx - shift)

        visible_weeks = self.available_weeks[start_idx:end_idx]

        # Створюємо нові кнопки
        for i, week in enumerate(visible_weeks):
            week_btn = QPushButton(str(week))
            week_btn.setObjectName(f"week_btn_{week}")
            week_btn.setFixedSize(50, 50)
            week_btn.setCheckable(True)
            week_btn.setChecked(week == self.current_week)

            week_btn.setStyleSheet("""
                QPushButton {
                    background-color: #333333;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 14px;
                    color: #DDDDDD;
                }
                QPushButton:checked {
                    background-color: #FF8C00;
                    color: white;
                }
                QPushButton:hover:!checked {
                    background-color: #444444;
                }
            """)

            # Зберігаємо тиждень як властивість кнопки
            week_btn.week = week

            # Створюємо локальну копію для замикання
            current_btn = week_btn
            current_btn.clicked.connect(lambda checked, b=current_btn: self.week_changed(b.week))

            # Вставляємо кнопку перед кнопкою "вперед"
            layout.insertWidget(i + 1, week_btn)
            self.week_btns.append(week_btn)

        # Оновлюємо стан кнопок
        self.update_buttons_state()

    def week_changed(self, week):
        """Обробка зміни тижня"""
        if week != self.current_week:
            logger.info(f"Зміна тижня: з {self.current_week} на {week}")

            # Зберігаємо новий поточний тиждень
            old_week = self.current_week
            self.current_week = week

            # Перевіряємо, чи потрібно оновити видимі кнопки
            current_index = self.available_weeks.index(week)
            visible_indices = [btn.week for btn in self.week_btns]

            # Якщо новий тиждень на краю або за межами видимого діапазону, оновлюємо UI
            if (week == min(visible_indices) or
                    week == max(visible_indices) or
                    week not in visible_indices):

                logger.info(f"Тиждень {week} на краю видимого діапазону. Оновлюємо UI.")
                self.update_ui_for_week(week)
            else:
                # Інакше просто оновлюємо стан кнопок
                self.update_buttons_state()

            # Викликаємо колбек, якщо він заданий
            if hasattr(self, 'on_week_change') and callable(self.on_week_change):
                self.on_week_change(week)

            # Випромінюємо сигнал про зміну тижня
            self.week_changed_signal.emit(week)

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
                self.week_changed(new_week)

    def next_week(self):
        """Перехід до наступного тижня"""
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            if current_index < len(self.available_weeks) - 1:
                new_week = self.available_weeks[current_index + 1]
                logger.info(f"Перехід до наступного тижня: {new_week}")
                self.week_changed(new_week)


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

        logger.info("Ініціалізація екрану тижнів вагітності")

        self.data_controller = DataController()
        self.baby_dev_controller = BabyDevelopmentController()

        self.current_week = self.data_controller.get_current_week() or 33
        self.available_weeks = self.baby_dev_controller.get_available_weeks()

        logger.info(f"Поточний тиждень вагітності: {self.current_week}")

        self.setup_ui()

    def setup_ui(self):
        # Головний layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Верхній заголовок
        header = QWidget()
        header.setObjectName("headerWidget")
        header.setMinimumHeight(60)
        header.setStyleSheet("background-color: #121212;")

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        if self.data_controller.get_days_left():
            days_text = f"{self.data_controller.get_days_left()} днів до пологів"
        else:
            days_text = "Дата пологів не встановлена"

        weeks_label = QLabel(days_text)
        weeks_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        weeks_label.setStyleSheet("color: #FF8C00;")
        # Зробимо текст адаптивним до ширини екрану
        weeks_label.setWordWrap(True)
        weeks_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        header_layout.addWidget(weeks_label)
        main_layout.addWidget(header)

        # Вміст сторінки у прокрутному вікні
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background-color: #000000;")
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Вимкнути горизонтальну прокрутку

        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        # Селектор тижнів
        self.week_selector = WeekSelector(
            current_week=self.current_week,
            available_weeks=self.available_weeks,
            on_week_change=self.update_content,
            parent=self
        )
        self.content_layout.addWidget(self.week_selector)

        # Секція інформаційних карток
        self.cards_section = QWidget()
        self.cards_section.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.cards_layout = QVBoxLayout(self.cards_section)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)

        # Додаємо секцію карток до контенту
        self.content_layout.addWidget(self.cards_section)

        # Заповнюємо картки для поточного тижня
        self.update_content(self.current_week)

        # Інформація про дитину
        self.baby_info_section = QFrame()
        self.baby_info_section.setProperty("card", True)
        self.baby_info_section.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.baby_info_section.setStyleSheet("""
            QFrame {
                background-color: #222222;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        baby_info_layout = QVBoxLayout(self.baby_info_section)

        # Заголовок "Ваша дитина"
        baby_title = QLabel("Ваша дитина")
        baby_title.setProperty("heading", True)
        baby_title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        baby_title.setStyleSheet("color: #FF8C00;")
        baby_info_layout.addWidget(baby_title)

        # Отримуємо інформацію про дитину
        child_info = self.data_controller.get_child_info()

        # Ім'я дитини (якщо вказано)
        if child_info["name"]:
            baby_name_label = QLabel(f"Ім'я: {child_info['name']}")
            baby_name_label.setFont(QFont('Arial', 12))
            baby_info_layout.addWidget(baby_name_label)

        # Стать дитини
        baby_gender_label = QLabel(f"Стать: {child_info['gender']}")
        baby_gender_label.setFont(QFont('Arial', 12))
        baby_info_layout.addWidget(baby_gender_label)

        # Дата пологів
        due_date_text = "Очікувана дата пологів: "
        if self.data_controller.pregnancy_data.due_date:
            due_date = self.data_controller.pregnancy_data.due_date.strftime("%d %B %Y")
            due_date_text += due_date
        else:
            due_date_text += "не встановлено"

        due_date_label = QLabel(due_date_text)
        due_date_label.setFont(QFont('Arial', 12))
        baby_info_layout.addWidget(due_date_label)

        # Додаємо інформацію про дитину до головного контенту
        self.content_layout.addWidget(self.baby_info_section)

        # Додаємо пусте місце внизу для прокрутки
        self.content_layout.addStretch(1)

        # Додаємо контент до прокрутного вікна
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        logger.info("Інтерфейс екрану тижнів налаштовано")

    def update_content(self, week):
        """Оновлює контент відповідно до вибраного тижня"""
        logger.info(f"Оновлення контенту для тижня {week}")

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