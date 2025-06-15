"""
Стилі для екрану тижнів вагітності
"""

from ..base import BaseStyles, Colors


class WeeksScreenStyles:
    @staticmethod
    def week_selector():
        """Селектор тижнів вгорі"""
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
                border-bottom: 1px solid {Colors.GLASS_BORDER};
                padding: 16px;
            }}
        """

    @staticmethod
    def week_button(color, size=60):
        """Кнопки тижнів"""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {color}, stop:1 {BaseStyles.darken_color(color.replace('#', ''), 0.3)});
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 {BaseStyles.lighten_color(color.replace('#', ''))}, stop:1 {color});
                border: 2px solid rgba(255, 255, 255, 0.4);
            }}
        """

    @staticmethod
    def nav_arrow_button():
        """Кнопки навігації стрілочки (без рамок)"""
        return f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 24px;
                font-weight: 700;
                color: white;
                font-size: 20px;
            }}
            QPushButton:disabled {{
                background: transparent;
                color: rgba(255, 255, 255, 0.3);
                border: none;
            }}
            QPushButton:hover:enabled {{
                background: rgba(255, 255, 255, 0.1);
                border: none;
            }}
        """

    @staticmethod
    def week_title_card():
        """Картка з заголовком тижня"""
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def week_title(color):
        """Заголовок тижня"""
        return f"""
            color: {color}; 
            font-size: 28px; 
            font-weight: 700;
        """

    @staticmethod
    def fruit_comparison_card():
        """Картка порівняння з фруктом"""
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def fruit_title():
        """Заголовок порівняння з фруктом"""
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
        """Опис порівняння з фруктом"""
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
        """Інформація про розмір"""
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

    @staticmethod
    def info_card():
        """Інформаційні картки"""
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 0px;
                margin: 0px;
            }}
            QFrame:hover {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid {Colors.GLASS_BORDER};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def info_card_base():
        """Базовий стиль для InfoCard"""
        return f"""
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
        """

    @staticmethod
    def info_card_hover():
        """Стиль для InfoCard при hover"""
        return f"""
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
        """

    @staticmethod
    def info_card_pressed():
        """Стиль для InfoCard при натисканні"""
        return f"""
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
        """

    @staticmethod
    def fruit_title_label():
        """Стиль для заголовка порівняння з фруктом"""
        return f"""
            color: {Colors.TEXT_PRIMARY}; 
            font-weight: 500; 
            line-height: 1.5; 
            padding: 12px 18px; 
            background: {Colors.GLASS_SURFACE}; 
            border: 1px solid {Colors.GLASS_BORDER}; 
            border-radius: 20px;
        """

    @staticmethod
    def fruit_description_label():
        """Стиль для опису порівняння з фруктом"""
        return f"""
            color: {Colors.TEXT_PRIMARY}; 
            font-weight: 500; 
            line-height: 1.5; 
            padding: 12px 18px; 
            background: {Colors.GLASS_SURFACE}; 
            border: 1px solid {Colors.GLASS_BORDER}; 
            border-radius: 20px;
        """