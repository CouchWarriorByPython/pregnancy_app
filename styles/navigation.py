"""
Стилі для навігації додатку
"""

from .base import Colors


class NavigationStyles:
    @staticmethod
    def bottom_nav():
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 0.05), stop:1 rgba(255, 255, 255, 0.02));
                border-top: 1px solid {Colors.GLASS_BORDER};
                backdrop-filter: blur(20px);
            }}
        """

    @staticmethod
    def nav_button():
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: {Colors.TEXT_SECONDARY};
                padding-top: 8px;
                padding-bottom: 8px;
                font-size: 11px;
                font-weight: 500;
                border-radius: 12px;
                margin: 4px;
            }}
            QPushButton:checked {{
                color: white;
                background: {Colors.PRIMARY_GRADIENT};
                font-weight: 700;
                transform: scale(1.05);
            }}
            QPushButton:hover:!checked {{
                color: {Colors.TEXT_PRIMARY};
                background: rgba(255, 255, 255, 0.1);
                transform: scale(1.02);
            }}
        """

    @staticmethod
    def main_layout():
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
            }}
        """

    @staticmethod
    def stack_widget():
        return f"""
            QStackedWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
            }}
        """