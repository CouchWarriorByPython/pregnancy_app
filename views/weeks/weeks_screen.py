from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QPushButton, QHBoxLayout,
                             QSizePolicy, QScrollArea, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from controllers.data_controller import DataController
from controllers.baby_development_controller import BabyDevelopmentController
from .fruit_comparison_view import FruitComparisonView
from utils.logger import get_logger
from utils.image_utils import generate_circle_image
from utils.styles import Styles

logger = get_logger('weeks_screen')


class InfoCard(QFrame):
    def __init__(self, title, content, icon_path=None, parent=None):
        super().__init__(parent)
        self.title_label = None
        self.content_label = None
        self.is_hover = False
        self.setup_ui(title, content, icon_path)
        self.setMouseTracking(True)

    def setup_ui(self, title, content, icon_path):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Styles.COLORS['surface']};
                border-radius: 15px;
                padding: 10px;
            }}
            QLabel {{
                color: {Styles.COLORS['text_primary']};
            }}
        """)

        card_layout = QVBoxLayout(self)
        header_layout = QHBoxLayout()

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

        if not icon_found:
            circle_pixmap = generate_circle_image(size=24, color=Styles.COLORS['primary'])
            icon_label.setPixmap(circle_pixmap)
            header_layout.addWidget(icon_label)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()

        card_layout.addLayout(header_layout)

        self.content_label = QLabel(content)
        self.content_label.setWordWrap(True)
        self.content_label.setFont(QFont('Arial', 12))
        self.content_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card_layout.addWidget(self.content_label)

        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def enterEvent(self, event):
        self.is_hover = True
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Styles.COLORS['surface_hover']};
                border-radius: 15px;
                padding: 10px;
                border: 1px solid {Styles.COLORS['primary']};
            }}
            QLabel {{
                color: {Styles.COLORS['text_primary']};
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hover = False
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Styles.COLORS['surface']};
                border-radius: 15px;
                padding: 10px;
                border: none;
            }}
            QLabel {{
                color: {Styles.COLORS['text_primary']};
            }}
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {Styles.COLORS['surface_variant']};
                    border-radius: 15px;
                    padding: 10px;
                    border: 1px solid {Styles.COLORS['primary']};
                }}
                QLabel {{
                    color: {Styles.COLORS['text_primary']};
                }}
            """)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_hover:
                self.setStyleSheet(f"""
                    QFrame {{
                        background-color: {Styles.COLORS['surface_hover']};
                        border-radius: 15px;
                        padding: 10px;
                        border: 1px solid {Styles.COLORS['primary']};
                    }}
                    QLabel {{
                        color: {Styles.COLORS['text_primary']};
                    }}
                """)
            else:
                self.setStyleSheet(f"""
                    QFrame {{
                        background-color: {Styles.COLORS['surface']};
                        border-radius: 15px;
                        padding: 10px;
                        border: none;
                    }}
                    QLabel {{
                        color: {Styles.COLORS['text_primary']};
                    }}
                """)
        super().mouseReleaseEvent(event)


class WeeksScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
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
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(int(r + (255 - r) * factor), 255)
        g = min(int(g + (255 - g) * factor), 255)
        b = min(int(b + (255 - b) * factor), 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_week_color(self, week):
        if week <= 13:
            return "#E91E63"
        elif week <= 27:
            return "#9C27B0"
        else:
            return "#3F51B5"

    def create_week_button(self, week, is_current=False):
        color = self.get_week_color(week)
        week_btn = QPushButton(str(week))
        week_btn.setObjectName(f"week_btn_{week}")
        week_btn.setFixedSize(60, 60)
        week_btn.setCheckable(True)
        week_btn.setChecked(is_current)
        week_btn.setStyleSheet(Styles.button_circular(color, 60))
        week_btn.week = week
        week_btn.clicked.connect(lambda checked, b=week_btn: self.week_changed(b.week))
        return week_btn

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        week_selector_section = QWidget()
        week_selector_section.setObjectName("week_selector_section")
        week_selector_section.setMaximumHeight(100)

        week_selector_layout = QHBoxLayout(week_selector_section)
        week_selector_layout.setContentsMargins(10, 10, 10, 10)

        self.prev_btn = QPushButton("<")
        self.prev_btn.setObjectName("prev_week_btn")
        self.prev_btn.setFixedSize(45, 45)
        self.prev_btn.setStyleSheet(Styles.button_nav_arrow())
        self.prev_btn.clicked.connect(self.prev_week)
        week_selector_layout.addWidget(self.prev_btn)

        current_index = self.get_current_week_index()
        visible_weeks = self.get_visible_weeks_range(current_index)

        self.week_btns = []
        for week in visible_weeks:
            week_btn = self.create_week_button(week, week == self.current_week)
            week_selector_layout.addWidget(week_btn)
            self.week_btns.append(week_btn)

        self.next_btn = QPushButton(">")
        self.next_btn.setObjectName("next_week_btn")
        self.next_btn.setFixedSize(45, 45)
        self.next_btn.setStyleSheet(Styles.button_nav_arrow())
        self.next_btn.clicked.connect(self.next_week)
        week_selector_layout.addWidget(self.next_btn)

        main_layout.addWidget(week_selector_section)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.scroll_area())

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        self.week_title = QLabel(f"Тиждень {self.current_week}")
        self.week_title.setObjectName("week_title_label")
        self.week_title.setFont(QFont('Arial', 22, QFont.Weight.Bold))
        self.week_title.setStyleSheet(Styles.text_accent())
        self.week_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.week_title)

        self.fruit_comparison_view = None

        cards_section = QWidget()
        self.cards_layout = QVBoxLayout(cards_section)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)

        self.content_layout.addWidget(cards_section)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.update_buttons_state()
        self.update_content(self.current_week)

    def get_current_week_index(self):
        if self.current_week in self.available_weeks:
            return self.available_weeks.index(self.current_week)

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
        total_buttons = 5
        half_range = total_buttons // 2

        start_idx = max(0, current_index - half_range)
        end_idx = min(len(self.available_weeks), start_idx + total_buttons)

        if end_idx - start_idx < total_buttons and start_idx > 0:
            shift = total_buttons - (end_idx - start_idx)
            start_idx = max(0, start_idx - shift)

        return self.available_weeks[start_idx:end_idx]

    def update_ui_for_week(self, week):
        logger.info(f"Оновлення UI тижнів для тижня {week}")

        for btn in self.week_btns:
            btn.deleteLater()
        self.week_btns.clear()

        week_selector_layout = None
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if widget and widget.objectName() == "week_selector_section":
                week_selector_layout = widget.layout()
                break

        if not week_selector_layout:
            logger.error("Не знайдено layout селектора тижнів")
            return

        for i in reversed(range(1, week_selector_layout.count() - 1)):
            item = week_selector_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                week_selector_layout.removeItem(item)

        if week in self.available_weeks:
            current_index = self.available_weeks.index(week)
        else:
            current_index = 0
            min_diff = abs(self.available_weeks[0] - week)
            for i, w in enumerate(self.available_weeks):
                diff = abs(w - week)
                if diff < min_diff:
                    min_diff = diff
                    current_index = i
            week = self.available_weeks[current_index]

        self.current_week = week
        visible_weeks = self.get_visible_weeks_range(current_index)

        for i, week in enumerate(visible_weeks):
            week_btn = self.create_week_button(week, week == self.current_week)
            week_selector_layout.insertWidget(i + 1, week_btn)
            self.week_btns.append(week_btn)

        self.update_buttons_state()

    def update_content(self, week):
        logger.info(f"Оновлення контенту для тижня {week}")

        if hasattr(self, 'week_title'):
            self.week_title.setText(f"Тиждень {week}")

        if self.current_displayed_week == week:
            logger.info(f"Тиждень {week} вже відображається, пропускаємо оновлення")
            return

        self.current_displayed_week = week

        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

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
        if week != self.current_week:
            logger.info(f"Зміна тижня: з {self.current_week} на {week}")
            old_week = self.current_week
            self.current_week = week
            self.update_buttons_state()
            self.update_content(week)

    def update_buttons_state(self):
        for btn in self.week_btns:
            btn.setChecked(btn.week == self.current_week)

        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            self.prev_btn.setEnabled(current_index > 0)
            self.next_btn.setEnabled(current_index < len(self.available_weeks) - 1)
        else:
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            logger.warning(f"Тиждень {self.current_week} не знайдено серед доступних")

    def prev_week(self):
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            if current_index > 0:
                new_week = self.available_weeks[current_index - 1]
                logger.info(f"Перехід до попереднього тижня: {new_week}")

                visible_weeks = [btn.week for btn in self.week_btns]
                if new_week not in visible_weeks or new_week == min(visible_weeks):
                    self.update_ui_for_week(new_week)

                self.week_changed(new_week)

    def next_week(self):
        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            if current_index < len(self.available_weeks) - 1:
                new_week = self.available_weeks[current_index + 1]
                logger.info(f"Перехід до наступного тижня: {new_week}")

                visible_weeks = [btn.week for btn in self.week_btns]
                if new_week not in visible_weeks or new_week == max(visible_weeks):
                    self.update_ui_for_week(new_week)

                self.week_changed(new_week)