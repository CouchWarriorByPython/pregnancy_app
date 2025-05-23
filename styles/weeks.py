"""
Стилі для екрану тижнів вагітності
"""

from .base import BaseStyles, Colors


class WeeksStyles:
    @staticmethod
    def week_button(color, size=60):
        return f"""
            QPushButton {{
                background-color: {color};
                border-radius: {size // 2}px;
                font-weight: bold;
                font-size: 18px;
                color: white;
                text-align: center;
            }}
            QPushButton:checked {{
                background-color: {Colors.PRIMARY};
                color: white;
            }}
            QPushButton:hover:!checked {{
                background-color: {BaseStyles.lighten_color(color)};
            }}
        """

    @staticmethod
    def nav_arrow_button():
        return f"""
            QPushButton {{
                background-color: {Colors.SURFACE_VARIANT};
                border-radius: 22px;
                font-weight: bold;
                color: #DDDDDD;
                font-size: 18px;
            }}
            QPushButton:disabled {{
                background-color: {Colors.SURFACE};
                color: {Colors.BORDER};
            }}
            QPushButton:hover:enabled {{
                background-color: {Colors.BORDER};
            }}
        """

    @staticmethod
    def fruit_comparison_card():
        return f"""
            QWidget {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }}
        """

    @staticmethod
    def info_card_base():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 10px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def info_card_hover():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE_HOVER};
                border-radius: 15px;
                padding: 10px;
                border: 1px solid {Colors.PRIMARY};
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def info_card_pressed():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE_VARIANT};
                border-radius: 15px;
                padding: 10px;
                border: 1px solid {Colors.PRIMARY};
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def week_title(color):
        return f"color: {color}; font-size: 22px; font-weight: bold;"