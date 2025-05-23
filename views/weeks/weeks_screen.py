from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QScrollArea, QFrame
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
        self.is_hover = False
        self._setup_ui(title, content, icon_path)
        self.setMouseTracking(True)

    def _setup_ui(self, title, content, icon_path):
        self.setStyleSheet(Styles.info_card_base())
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        header_layout = QHBoxLayout()
        icon_label = self._create_icon(icon_path)

        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Weight.Bold))

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setFont(QFont('Arial', 12))
        content_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addLayout(header_layout)
        layout.addWidget(content_label)
        layout.addStretch()
        self.setMinimumHeight(100)

    def _create_icon(self, icon_path):
        icon_label = QLabel()
        try:
            if icon_path:
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    icon_label.setPixmap(pixmap.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio))
                    return icon_label
        except Exception as e:
            logger.error(f"Помилка завантаження іконки: {e}")

        icon_label.setPixmap(generate_circle_image(size=24, color=Styles.COLORS['primary']))
        return icon_label

    def enterEvent(self, event):
        self.is_hover = True
        self.setStyleSheet(Styles.info_card_hover())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hover = False
        self.setStyleSheet(Styles.info_card_base())
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet(Styles.info_card_pressed())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            style = Styles.info_card_hover() if self.is_hover else Styles.info_card_base()
            self.setStyleSheet(style)
        super().mouseReleaseEvent(event)


class WeeksScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("Ініціалізація екрану тижнів вагітності")

        self.data_controller = DataController()
        self.baby_dev_controller = BabyDevelopmentController()

        self.current_week = self.data_controller.get_current_week() or 33
        self.available_weeks = self.baby_dev_controller.get_available_weeks()
        self.current_displayed_week = None
        self.week_btns = []

        logger.info(f"Поточний тиждень вагітності: {self.current_week}")
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._create_week_selector())
        main_layout.addWidget(self._create_content_area())

        self._update_buttons_state()
        self.update_content(self.current_week)

    def _create_week_selector(self):
        week_selector = QWidget()
        week_selector.setMaximumHeight(100)
        layout = QHBoxLayout(week_selector)
        layout.setContentsMargins(10, 10, 10, 10)

        self.prev_btn = self._create_nav_button("<", self.prev_week)
        layout.addWidget(self.prev_btn)

        current_index = self._get_current_week_index()
        visible_weeks = self._get_visible_weeks_range(current_index)

        for week in visible_weeks:
            week_btn = self._create_week_button(week, week == self.current_week)
            layout.addWidget(week_btn)
            self.week_btns.append(week_btn)

        self.next_btn = self._create_nav_button(">", self.next_week)
        layout.addWidget(self.next_btn)

        return week_selector

    def _create_nav_button(self, text, callback):
        button = QPushButton(text)
        button.setFixedSize(45, 45)
        button.setStyleSheet(Styles.button_nav_arrow())
        button.clicked.connect(callback)
        return button

    def _create_week_button(self, week, is_current=False):
        color = self._get_week_color(week)
        week_btn = QPushButton(str(week))
        week_btn.setFixedSize(60, 60)
        week_btn.setCheckable(True)
        week_btn.setChecked(is_current)
        week_btn.setStyleSheet(Styles.button_circular(color, 60))
        week_btn.week = week
        week_btn.clicked.connect(lambda: self.week_changed(week))
        return week_btn

    def _get_week_color(self, week):
        if week <= 13:
            return "#E91E63"
        elif week <= 27:
            return "#9C27B0"
        else:
            return "#3F51B5"

    def _create_content_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.scroll_area())

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(15)

        self.week_title = QLabel(f"Тиждень {self.current_week}")
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
        return scroll_area

    def _get_current_week_index(self):
        if self.current_week in self.available_weeks:
            return self.available_weeks.index(self.current_week)

        current_index = min(range(len(self.available_weeks)),
                            key=lambda i: abs(self.available_weeks[i] - self.current_week))
        self.current_week = self.available_weeks[current_index]
        return current_index

    def _get_visible_weeks_range(self, current_index):
        total_buttons = 5
        half_range = total_buttons // 2
        start_idx = max(0, current_index - half_range)
        end_idx = min(len(self.available_weeks), start_idx + total_buttons)

        if end_idx - start_idx < total_buttons and start_idx > 0:
            start_idx = max(0, start_idx - (total_buttons - (end_idx - start_idx)))

        return self.available_weeks[start_idx:end_idx]

    def update_content(self, week):
        logger.info(f"Оновлення контенту для тижня {week}")

        if self.current_displayed_week == week:
            return

        self.current_displayed_week = week
        self.week_title.setText(f"Тиждень {week}")

        self._clear_cards()
        self._update_fruit_comparison(week)
        self._create_info_cards(week)

    def _clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def _update_fruit_comparison(self, week):
        child_info = self.data_controller.get_child_info()
        fruit_data = self.baby_dev_controller.get_fruit_comparison(week)
        size_data = self.baby_dev_controller.get_baby_size(week)

        if fruit_data:
            fruit_data.update(size_data)
            if self.fruit_comparison_view:
                self.fruit_comparison_view.update_fruit_data(week, fruit_data)
            else:
                self.fruit_comparison_view = FruitComparisonView(week, fruit_data)
                self.content_layout.insertWidget(1, self.fruit_comparison_view)

    def _create_info_cards(self, week):
        child_info = self.data_controller.get_child_info()

        cards_data = [
            {
                "title": "Зростання вашої дитини",
                "content": self.baby_dev_controller.get_baby_development_info(week, child_info["gender"]),
                "icon": "resources/images/icons/development.png"
            },
            {
                "title": "Все про вас",
                "content": self.baby_dev_controller.get_mother_changes_info(week),
                "icon": "resources/images/icons/symptoms.png"
            },
            {
                "title": "Поради щодо харчування",
                "content": self.baby_dev_controller.get_nutrition_tips(week),
                "icon": "resources/images/icons/nutrition.png"
            },
            {
                "title": "Поради для вашого терміну",
                "content": "На цьому тижні важливо слідкувати за своїм здоров'ям та відвідувати лікаря за розкладом.",
                "icon": "resources/images/icons/tips.png"
            }
        ]

        for card_data in cards_data:
            card = InfoCard(card_data["title"], card_data["content"], card_data.get("icon"))
            self.cards_layout.addWidget(card)

    def week_changed(self, week):
        if week != self.current_week:
            logger.info(f"Зміна тижня: з {self.current_week} на {week}")
            self.current_week = week
            self._update_buttons_state()
            self.update_content(week)

    def _update_buttons_state(self):
        for btn in self.week_btns:
            btn.setChecked(btn.week == self.current_week)

        if self.current_week in self.available_weeks:
            current_index = self.available_weeks.index(self.current_week)
            self.prev_btn.setEnabled(current_index > 0)
            self.next_btn.setEnabled(current_index < len(self.available_weeks) - 1)

    def _navigate_week(self, direction):
        if self.current_week not in self.available_weeks:
            return

        current_index = self.available_weeks.index(self.current_week)
        new_index = current_index + direction

        if 0 <= new_index < len(self.available_weeks):
            new_week = self.available_weeks[new_index]
            visible_weeks = [btn.week for btn in self.week_btns]

            if new_week not in visible_weeks or (direction == -1 and new_week == min(visible_weeks)) or (
                    direction == 1 and new_week == max(visible_weeks)):
                self._update_ui_for_week(new_week)

            self.week_changed(new_week)

    def prev_week(self):
        self._navigate_week(-1)

    def next_week(self):
        self._navigate_week(1)

    def _update_ui_for_week(self, week):
        for btn in self.week_btns:
            btn.deleteLater()
        self.week_btns.clear()

        week_selector_layout = self.layout().itemAt(0).widget().layout()

        for i in reversed(range(1, week_selector_layout.count() - 1)):
            item = week_selector_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        current_index = self._get_current_week_index() if week in self.available_weeks else 0
        self.current_week = week
        visible_weeks = self._get_visible_weeks_range(current_index)

        for i, week in enumerate(visible_weeks):
            week_btn = self._create_week_button(week, week == self.current_week)
            week_selector_layout.insertWidget(i + 1, week_btn)
            self.week_btns.append(week_btn)

        self._update_buttons_state()