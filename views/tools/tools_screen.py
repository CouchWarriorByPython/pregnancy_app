from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QScrollArea, QFrame, QGridLayout, QSizePolicy,
                             QMessageBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from controllers.data_controller import DataController
from utils.styles import Styles

from .health_report import HealthReportScreen
from .kegel_exercises import KegelExercisesScreen
from .weight_monitor import WeightMonitorScreen
from .kick_counter import KickCounterScreen
from .contraction_counter import ContractionCounterScreen
from .belly_tracker import BellyTrackerScreen
from .blood_pressure_monitor import BloodPressureMonitorScreen
from .wishlist import WishlistScreen


class ToolCard(QFrame):
    def __init__(self, title, description, icon_path, screen_class, accent_color="#FF8C00", parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.icon_path = icon_path
        self.accent_color = accent_color
        self.screen_class = screen_class
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(Styles.tool_card_base())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        icon_label = QLabel()
        try:
            pixmap = QPixmap(self.icon_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(pixmap)
                icon_label.setFixedSize(40, 40)
                icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                icon_label.setText("🔧")
                icon_label.setStyleSheet(Styles.tool_icon_fallback(self.accent_color))
                icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            icon_label.setText("🔧")
            icon_label.setStyleSheet(Styles.tool_icon_fallback(self.accent_color))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(self.title)
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title_label.setStyleSheet(Styles.tool_card_title(self.accent_color))

        desc_label = QLabel(self.description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(Styles.tool_card_description())
        desc_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        header_layout = QHBoxLayout()
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)
        layout.addWidget(desc_label)
        layout.addStretch()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.screen_class:
            try:
                tool_screen = self.screen_class(self.parent)

                if hasattr(self.parent, 'parent') and self.parent.parent:
                    main_window = self.parent.parent

                    main_stack = None
                    for child in main_window.findChildren(QStackedWidget):
                        main_stack = child
                        break

                    if main_stack:
                        index = main_stack.addWidget(tool_screen)
                        main_stack.setCurrentIndex(index)
                    else:
                        QMessageBox.warning(self, "Помилка", "Не вдалося відкрити інструмент")
                else:
                    QMessageBox.warning(self, "Помилка", "Не вдалося відкрити інструмент")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити інструмент: {str(e)}")


class ToolsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setMinimumHeight(60)
        header.setStyleSheet(Styles.header())

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 5, 15, 5)

        tools_label = QLabel("Інструменти")
        tools_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        tools_label.setStyleSheet(Styles.text_accent())

        header_layout.addWidget(tools_label)
        main_layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(Styles.scroll_area())
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(15)

        cards_grid = QGridLayout()
        cards_grid.setSpacing(15)

        tools_data = [
            {
                "title": "Звіт про здоров'я в PDF",
                "description": "Створіть PDF-звіт із усіма показниками вашого здоров'я за вибраний період.",
                "icon": "resources/images/tools/health_report.png",
                "accent_color": "#FF5252",
                "screen_class": HealthReportScreen
            },
            {
                "title": "Вправи Кегеля",
                "description": "Інструкції та таймер для виконання вправ Кегеля протягом вагітності.",
                "icon": "resources/images/tools/kegel.png",
                "accent_color": "#9C27B0",
                "screen_class": KegelExercisesScreen
            },
            {
                "title": "Монітор ваги",
                "description": "Відстежуйте зміни ваги протягом вагітності. Поточна вага: 65.1 кг",
                "icon": "resources/images/tools/weight_monitor.png",
                "accent_color": "#757575",
                "screen_class": WeightMonitorScreen
            },
            {
                "title": "Лічильник поштовхів",
                "description": "Рахуйте і записуйте поштовхи дитини для моніторингу її активності.",
                "icon": "resources/images/tools/kick_counter.png",
                "accent_color": "#4CAF50",
                "screen_class": KickCounterScreen
            },
            {
                "title": "Лічильник переймів",
                "description": "Вимірюйте частоту та тривалість переймів під час підготовки до пологів.",
                "icon": "resources/images/tools/contraction_counter.png",
                "accent_color": "#2196F3",
                "screen_class": ContractionCounterScreen
            },
            {
                "title": "Відстеження розміру живота",
                "description": "Записуйте зміни розміру живота, щоб відстежувати ріст дитини.",
                "icon": "resources/images/tools/belly_growth.png",
                "accent_color": "#FF9800",
                "screen_class": BellyTrackerScreen
            },
            {
                "title": "Монітор тиску",
                "description": "Контролюйте артеріальний тиск протягом вагітності.",
                "icon": "resources/images/tools/pressure_monitor.png",
                "accent_color": "#E91E63",
                "screen_class": BloodPressureMonitorScreen
            },
            {
                "title": "Список бажань",
                "description": "Створіть список речей, які потрібно придбати для вас та дитини.",
                "icon": "resources/images/tools/wishlist.png",
                "accent_color": "#673AB7",
                "screen_class": WishlistScreen
            }
        ]

        row, col = 0, 0
        for i, tool in enumerate(tools_data):
            card = ToolCard(
                title=tool["title"],
                description=tool["description"],
                icon_path=tool["icon"],
                accent_color=tool["accent_color"],
                screen_class=tool["screen_class"],
                parent=self
            )
            cards_grid.addWidget(card, row, col)

            col += 1
            if col > 1:
                col = 0
                row += 1

        content_layout.addLayout(cards_grid)
        content_layout.addStretch(1)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)