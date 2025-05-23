"""
Стилі для екрану тижнів вагітності
"""

from .base import BaseStyles, Colors


class WeeksStyles:
    @staticmethod
    def week_button(color, size=60):
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {color}, stop:1 {BaseStyles.darken_color(color.replace('#', ''), 0.3)});
                border-radius: {size // 2}px;
                font-weight: 700;
                font-size: 16px;
                color: white;
                text-align: center;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }}
            QPushButton:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 3px solid white;
                color: white;
            }}
            QPushButton:hover:!checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {BaseStyles.lighten_color(color.replace('#', ''))}, stop:1 {color});
                border: 2px solid rgba(255, 255, 255, 0.4);
            }}
        """

    @staticmethod
    def nav_arrow_button():
        return f"""
            QPushButton {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                font-weight: 700;
                color: white;
                font-size: 20px;
            }}
            QPushButton:disabled {{
                background: rgba(255, 255, 255, 0.05);
                color: rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            QPushButton:hover:enabled {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
        """

    @staticmethod
    def fruit_comparison_card():
        return f"""
            QWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 24px;
                margin: 16px;
            }}
        """

    @staticmethod
    def info_card_base():
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 0px;
                margin: 8px;
            }}
        """

    @staticmethod
    def info_card_hover():
        return f"""
            QFrame {{
                background: {Colors.SURFACE_HOVER};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 20px;
                padding: 0px;
                margin: 8px;
            }}
        """

    @staticmethod
    def info_card_pressed():
        return f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.25);
                border: 2px solid {Colors.PRIMARY};
                border-radius: 20px;
                padding: 0px;
                margin: 8px;
            }}
        """

    @staticmethod
    def week_title(color):
        return f"""
            color: {color}; 
            font-size: 24px; 
            font-weight: 700;
        """

    @staticmethod
    def week_selector():
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
                border-bottom: 1px solid {Colors.GLASS_BORDER};
                padding: 16px;
            }}
        """

    @staticmethod
    def fruit_title():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 20px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 16px;
            }}
        """

    @staticmethod
    def fruit_description():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                font-weight: 500;
                text-align: center;
                margin: 12px 0;
                line-height: 1.4;
            }}
        """

    @staticmethod
    def fruit_size_info():
        return f"""
            QLabel {{
                color: {Colors.TEXT_ACCENT};
                font-size: 13px;
                font-weight: 600;
                text-align: center;
                background: rgba(139, 92, 246, 0.2);
                padding: 8px 16px;
                border-radius: 12px;
                border: 1px solid rgba(139, 92, 246, 0.3);
            }}
        """