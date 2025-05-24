from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
                             QFrame, QGridLayout, QSizePolicy, QMessageBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

from controllers.data_controller import DataController
from styles.tools import ToolsStyles
from styles.base import BaseStyles, Colors

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
        self.screen_class = screen_class
        self.parent = parent
        self.accent_color = accent_color
        self.title = title
        self.description = description
        self._setup_ui()
        self.setMouseTracking(True)

    def _setup_ui(self):
        # Встановлюємо стиль для всього зовнішнього контейнера
        self.setStyleSheet(f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)

        # Зменшуємо розмір картки
        self.setFixedHeight(120)

        # Єдиний layout для всього вмісту
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        # Заголовок
        title_label = QLabel(self.title)
        title_label.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {self.accent_color}; font-weight: 700; background: transparent;")
        layout.addWidget(title_label)

        # Опис
        description_label = QLabel(self.description)
        description_label.setWordWrap(True)
        description_label.setFont(QFont('Arial', 13))
        description_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: 500; background: transparent;")
        layout.addWidget(description_label)

    def enterEvent(self, event):
        self.is_hover = True
        self.setStyleSheet(f"""
            QFrame {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hover = False
        self.setStyleSheet(f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setStyleSheet(f"""
                QFrame {{
                    background: rgba(255, 255, 255, 0.25);
                    border: 1px solid {Colors.GLASS_BORDER};
                    border-radius: 24px;
                    padding: 0px;
                    margin: 0px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            style = f"""
                QFrame {{
                    background: {Colors.SURFACE_HOVER if self.is_hover else Colors.GLASS_SURFACE};
                    border: 1px solid {Colors.GLASS_BORDER};
                    border-radius: 24px;
                    padding: 0px;
                    margin: 0px;
                }}
                QLabel {{
                    background: transparent;
                    border: none;
                }}
            """
            self.setStyleSheet(style)

            if self.screen_class:
                try:
                    tool_screen = self.screen_class(self.parent)
                    main_stack = self._find_main_stack()

                    if main_stack:
                        index = main_stack.addWidget(tool_screen)
                        main_stack.setCurrentIndex(index)
                    else:
                        QMessageBox.warning(self, "Помилка", "Не вдалося відкрити інструмент")
                except Exception as e:
                    QMessageBox.critical(self, "Помилка", f"Не вдалося відкрити інструмент: {str(e)}")
        super().mouseReleaseEvent(event)

    def _find_main_stack(self):
        if hasattr(self.parent, 'parent') and self.parent.parent:
            for child in self.parent.parent.findChildren(QStackedWidget):
                return child
        return None


class ToolsScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_controller = DataController()
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
            ("Звіт про здоров'я в PDF", "Створіть PDF-звіт із усіма показниками вашого здоров'я за вибраний період.",
             "resources/images/tools/health_report.png", "#FF5252", HealthReportScreen),
            ("Вправи Кегеля", "Інструкції та таймер для виконання вправ Кегеля протягом вагітності.",
             "resources/images/tools/kegel.png", "#9C27B0", KegelExercisesScreen),
            ("Монітор ваги", "Відстежуйте зміни ваги протягом вагітності. Поточна вага: 65.1 кг",
             "resources/images/tools/weight_monitor.png", "#757575", WeightMonitorScreen),
            ("Лічильник поштовхів", "Рахуйте і записуйте поштовхи дитини для моніторингу її активності.",
             "resources/images/tools/kick_counter.png", "#4CAF50", KickCounterScreen),
            ("Лічильник переймів", "Вимірюйте частоту та тривалість переймів під час підготовки до пологів.",
             "resources/images/tools/contraction_counter.png", "#2196F3", ContractionCounterScreen),
            ("Відстеження розміру живота", "Записуйте зміни розміру живота, щоб відстежувати ріст дитини.",
             "resources/images/tools/belly_growth.png", "#FF9800", BellyTrackerScreen),
            ("Монітор тиску", "Контролюйте артеріальний тиск протягом вагітності.",
             "resources/images/tools/pressure_monitor.png", "#E91E63", BloodPressureMonitorScreen),
            ("Список бажань", "Створіть список речей, які потрібно придбати для вас та дитини.",
             "resources/images/tools/wishlist.png", "#673AB7", WishlistScreen)
        ]

        for i, (title, description, icon, color, screen_class) in enumerate(tools_data):
            card = ToolCard(title, description, icon, screen_class, color, self)
            cards_grid.addWidget(card, i // 2, i % 2)

        return cards_grid