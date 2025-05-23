from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controllers.data_controller import DataController
from controllers.baby_development_controller import BabyDevelopmentController
from .fruit_comparison_view import FruitComparisonView
from utils.logger import get_logger
from styles.weeks import WeeksStyles
from styles.base import BaseStyles, Colors

logger = get_logger('weeks_screen')


class InfoCard(QFrame):
    def __init__(self, title, content, parent=None):
        super().__init__(parent)
        self.is_hover = False
        self._setup_ui(title, content)
        self.setMouseTracking(True)

    def _setup_ui(self, title, content):
        self.setStyleSheet(WeeksStyles.info_card_base())
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {Colors.TEXT_ACCENT}; font-weight: 700;")

        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setFont(QFont('Arial', 14))
        content_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 500; line-height: 1.5;")
        content_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(title_label)
        layout.addWidget(content_label)
        layout.addStretch()
        self.setMinimumHeight(120)

    def enterEvent(self, event):
        self.is_hover = True
        self.setStyleSheet(WeeksStyles.info_card_hover())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hover = False
        self.setStyleSheet(WeeksStyles.info_card_base())
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet(WeeksStyles.info_card_pressed())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            style = WeeksStyles.info_card_hover() if self.is_hover else WeeksStyles.info_card_base()
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
        week_selector.setStyleSheet(WeeksStyles.week_selector())
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
        button.setStyleSheet(WeeksStyles.nav_arrow_button())
        button.clicked.connect(callback)
        return button

    def _create_week_button(self, week, is_current=False):
        color = self._get_week_color(week)
        week_btn = QPushButton(str(week))
        week_btn.setFixedSize(60, 60)
        week_btn.setCheckable(True)
        week_btn.setChecked(is_current)
        week_btn.setStyleSheet(WeeksStyles.week_button(color, 60))
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
        scroll_area.setStyleSheet(BaseStyles.scroll_area())

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(16)

        content_container = QWidget()
        content_container.setMaximumWidth(800)
        self.inner_layout = QVBoxLayout(content_container)
        self.inner_layout.setContentsMargins(0, 0, 0, 0)
        self.inner_layout.setSpacing(16)

        self.week_title_card = self._create_week_title_card()
        self.inner_layout.addWidget(self.week_title_card)

        self.fruit_comparison_view = None

        cards_section = QWidget()
        self.cards_layout = QVBoxLayout(cards_section)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(12)

        self.inner_layout.addWidget(cards_section)

        layout_container = QHBoxLayout()
        layout_container.addStretch()
        layout_container.addWidget(content_container)
        layout_container.addStretch()
        self.content_layout.addLayout(layout_container)

        scroll_area.setWidget(content_widget)
        return scroll_area

    def _create_week_title_card(self):
        title_card = QFrame()
        title_card.setStyleSheet(WeeksStyles.week_title_card())
        title_layout = QVBoxLayout(title_card)
        title_layout.setContentsMargins(30, 30, 30, 30)

        self.week_title = QLabel(f"Тиждень {self.current_week}")
        self.week_title.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        self.week_title.setStyleSheet(WeeksStyles.week_title(Colors.TEXT_ACCENT))
        self.week_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.week_title)

        return title_card

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
                self.inner_layout.insertWidget(1, self.fruit_comparison_view)

    def _create_info_cards(self, week):
        child_info = self.data_controller.get_child_info()

        cards_data = [
            {
                "title": "Зростання вашої дитини",
                "content": self.baby_dev_controller.get_baby_development_info(week, child_info["gender"])
            },
            {
                "title": "Все про вас",
                "content": self.baby_dev_controller.get_mother_changes_info(week)
            },
            {
                "title": "Поради щодо харчування",
                "content": self.baby_dev_controller.get_nutrition_tips(week)
            },
            {
                "title": "Поради для вашого терміну",
                "content": "На цьому тижні важливо слідкувати за своїм здоров'ям та відвідувати лікаря за розкладом."
            }
        ]

        for card_data in cards_data:
            card = InfoCard(card_data["title"], card_data["content"])
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

            self.current_week = new_week

            visible_weeks = [btn.week for btn in self.week_btns]
            if new_week not in visible_weeks:
                self._rebuild_week_buttons()

            self.update_content(new_week)
            self._update_buttons_state()

    def _rebuild_week_buttons(self):
        for btn in self.week_btns:
            btn.deleteLater()
        self.week_btns.clear()

        week_selector_layout = self.layout().itemAt(0).widget().layout()

        for i in reversed(range(1, week_selector_layout.count() - 1)):
            item = week_selector_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        current_index = self.available_weeks.index(self.current_week)
        visible_weeks = self._get_visible_weeks_range(current_index)

        for i, week in enumerate(visible_weeks):
            week_btn = self._create_week_button(week, week == self.current_week)
            week_selector_layout.insertWidget(i + 1, week_btn)
            self.week_btns.append(week_btn)

    def prev_week(self):
        self._navigate_week(-1)

    def next_week(self):
        self._navigate_week(1)