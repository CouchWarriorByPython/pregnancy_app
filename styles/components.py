"""
Стилі для перев компонентів UI
"""

from .base import Colors


class ComponentStyles:
    @staticmethod
    def styled_card(accent_color=None):
        """Універсальний стиль для карток"""
        accent = accent_color or Colors.GLASS_BORDER
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {accent};
                border-radius: 24px;
                padding: 24px;
                margin: 12px;
            }}
            QLabel {{
                background: transparent;
                border: none;
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                line-height: 1.5;
            }}
        """

    @staticmethod
    def info_card():
        """Стиль для інформаційних карток"""
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 24px;
                padding: 30px;
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
    def form_section():
        """Стиль для секцій форм"""
        return f"""
            QWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 24px;
                margin: 12px;
            }}
        """

    @staticmethod
    def date_edit():
        """Стиль для віджетів вибору дати"""
        return f"""
            QDateEdit {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 16px 20px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 20px;
            }}
            QDateEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
                background: rgba(255, 255, 255, 0.12);
            }}
            QDateEdit::drop-down {{
                border: none;
                width: 30px;
                background: transparent;
            }}
            QDateEdit::down-arrow {{
                image: none;
                border: 5px solid transparent;
                border-top: 8px solid {Colors.TEXT_PRIMARY};
                margin-right: 10px;
            }}
            QCalendarWidget {{
                background: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 8px;
            }}
            QCalendarWidget QToolButton {{
                color: {Colors.TEXT_PRIMARY};
                background: transparent;
                border: none;
                border-radius: 4px;
                padding: 4px;
            }}
            QCalendarWidget QToolButton:hover {{
                background: rgba(255, 255, 255, 0.1);
            }}
            QCalendarWidget QMenu {{
                background: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
            }}
            QCalendarWidget QSpinBox {{
                background: transparent;
                color: {Colors.TEXT_PRIMARY};
                border: none;
            }}
            QCalendarWidget QAbstractItemView {{
                background: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
                selection-color: white;
            }}
        """

    @staticmethod
    def info_label():
        """Стиль для інформаційних підписів"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-weight: 400;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def field_label():
        """Стиль для підписів полів"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def disabled_field():
        """Стиль для неактивних полів"""
        return f"""
            QLabel {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                padding: 16px 20px;
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                min-height: 20px;
            }}
        """

    @staticmethod
    def info_box(accent_color=None):
        """Стиль для інформаційних блоків"""
        accent = accent_color or Colors.PRIMARY
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background: rgba(255, 255, 255, 0.08);
                padding: 20px;
                border-radius: 16px;
                border: 1px solid {accent};
                font-size: 14px;
                font-weight: 500;
                line-height: 1.6;
            }}
        """

    @staticmethod
    def colored_section(color):
        """Стиль для кольорових секцій"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba({color}, 0.1), stop:1 rgba({color}, 0.05));
                border: 1px solid rgba({color}, 0.3);
                border-radius: 20px;
                padding: 24px;
                margin: 12px 0;
            }}
        """