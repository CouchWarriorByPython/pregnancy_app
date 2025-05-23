"""
Стилі для навігації додатку
"""

from .base import Colors


class NavigationStyles:
    @staticmethod
    def bottom_nav():
        return f"background-color: {Colors.BACKGROUND};"

    @staticmethod
    def nav_button():
        return f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                color: #888888;
                padding-top: 5px;
                font-size: 10px;
            }}
            QPushButton:checked {{
                color: {Colors.PRIMARY};
            }}
            QPushButton:hover {{
                color: #AAAAAA;
            }}
        """

    @staticmethod
    def main_layout():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
            }}
        """

    @staticmethod
    def stack_widget():
        return f"""
            QStackedWidget {{
                background-color: {Colors.BACKGROUND};
            }}
        """