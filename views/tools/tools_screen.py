from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
                             QFrame, QGridLayout, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from styles import BaseStyles, ToolsScreenStyles
from utils.user_mixin import UserMixin

from .health_report import HealthReportScreen
from .kegel_exercises import KegelExercisesScreen
from .weight_monitor import WeightMonitorScreen
from .kick_counter import KickCounterScreen
from .contraction_counter import ContractionCounterScreen
from .belly_tracker import BellyTrackerScreen
from .blood_pressure_monitor import BloodPressureMonitorScreen
from .wishlist import WishlistScreen


class ToolCard(QFrame, UserMixin):
    def __init__(self, title, description, screen_class, accent_color="#FF8C00", parent=None):
        super().__init__(parent)
        self.screen_class = screen_class
        self.parent = parent
        self.accent_color = accent_color
        self.title = title
        self.description = description
        self.is_hover = False
        self._setup_ui()
        self.setMouseTracking(True)

    def _setup_ui(self):
        self.setStyleSheet(ToolsScreenStyles.tool_card())
        self.setFixedHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        title_label = QLabel(self.title)
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title_label.setStyleSheet(ToolsScreenStyles.tool_card_title(self.accent_color))
        layout.addWidget(title_label)

        description_label = QLabel(self.description)
        description_label.setWordWrap(True)
        description_label.setFont(QFont('Arial', 13))
        description_label.setStyleSheet(ToolsScreenStyles.tool_card_description())
        layout.addWidget(description_label)

    def enterEvent(self, event):
        self.is_hover = True
        self.setStyleSheet(ToolsScreenStyles.tool_card_hover())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hover = False
        self.setStyleSheet(ToolsScreenStyles.tool_card())
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet(ToolsScreenStyles.tool_card_pressed())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_hover:
                self.setStyleSheet(ToolsScreenStyles.tool_card_hover())
            else:
                self.setStyleSheet(ToolsScreenStyles.tool_card())

            if self.screen_class:
                try:
                    tool_screen = self.screen_class(self.parent)
                    main_window = self._find_main_window()

                    if main_window and hasattr(main_window, 'stack_widget'):
                        index = main_window.stack_widget.addWidget(tool_screen)
                        main_window.stack_widget.setCurrentIndex(index)
                    else:
                        QMessageBox.warning(self, "Помилка", "Не вдалося відкрити інструмент")
                except Exception as e:
                    QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити інструмент: {str(e)}")
        super().mouseReleaseEvent(event)


class ToolsScreen(QWidget, UserMixin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._create_header())
        main_layout.addWidget(self._create_content())

    def _create_header(self):
        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet(BaseStyles.header())

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        tools_label = QLabel("Інструменти")
        tools_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        tools_label.setStyleSheet(BaseStyles.text_accent())
        tools_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(tools_label)

        return header

    def _create_content(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(BaseStyles.scroll_area())
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        cards_grid = self._create_tools_grid()
        content_layout.addLayout(cards_grid)
        content_layout.addStretch(1)

        scroll_area.setWidget(content_widget)
        return scroll_area

    def _create_tools_grid(self):
        cards_grid = QGridLayout()
        cards_grid.setSpacing(15)

        tools_data = [
            ("Звіт про здоров'я", "Створіть PDF-звіт із усіма показниками вашого здоров'я за період", "#FF5252",
             HealthReportScreen),
            ("Вправи Кегеля", "Інструкції та таймер для виконання вправ Кегеля протягом вагітності", "#9C27B0",
             KegelExercisesScreen),
            ("Монітор ваги", "Відстежуйте зміни ваги протягом вагітності", "#757575", WeightMonitorScreen),
            ("Лічильник поштовхів", "Рахуйте і записуйте поштовхи дитини для моніторингу активності", "#4CAF50",
             KickCounterScreen),
            ("Лічильник переймів", "Вимірюйте частоту та тривалість переймів під час підготовки до пологів", "#2196F3",
             ContractionCounterScreen),
            ("Розмір живота", "Записуйте зміни розміру живота, щоб відстежувати ріст дитини", "#FF9800",
             BellyTrackerScreen),
            ("Монітор тиску", "Контролюйте артеріальний тиск протягом вагітності", "#E91E63",
             BloodPressureMonitorScreen),
            ("Список бажань", "Створіть список речей, які потрібно придбати для вас та дитини", "#673AB7",
             WishlistScreen)
        ]

        for i, (title, description, color, screen_class) in enumerate(tools_data):
            card = ToolCard(title, description, screen_class, color, self)
            cards_grid.addWidget(card, i // 2, i % 2)

        return cards_grid

    def showEvent(self, event):
        super().showEvent(event)
        self.init_data_controller()