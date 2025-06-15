"""
Стилі для екрану календаря
"""

from ..base import Colors


class CalendarScreenStyles:
    @staticmethod
    def calendar_widget():
        """Основний віджет календаря"""
        return f"""
            QCalendarWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                padding: 16px;
            }}
            QCalendarWidget QToolButton {{
                color: {Colors.TEXT_PRIMARY};
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 12px;
                padding: 8px 16px;
                font-weight: 600;
                margin: 4px;
            }}
            QCalendarWidget QToolButton:hover {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid {Colors.PRIMARY};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {Colors.TEXT_PRIMARY};
                background: transparent;
                selection-background-color: {Colors.PRIMARY};
                selection-color: white;
                font-weight: 500;
            }}
            QCalendarWidget QAbstractItemView::item {{
                padding: 8px;
                border-radius: 8px;
                margin: 2px;
            }}
            QCalendarWidget QAbstractItemView::item:hover {{
                background: rgba(255, 255, 255, 0.1);
            }}
            QCalendarWidget QAbstractItemView::item:selected {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                font-weight: 700;
            }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background: transparent;
                border: none;
            }}
            QCalendarWidget QSpinBox {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 8px;
                padding: 4px 8px;
                color: {Colors.TEXT_PRIMARY};
                font-weight: 600;
            }}
        """

    @staticmethod
    def event_dialog():
        """Діалог додавання події (без рамки)"""
        return f"""
            QDialog {{
                background: {Colors.BACKGROUND_GRADIENT};
                color: {Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 20px;
            }}
        """

    @staticmethod
    def event_dialog_title():
        """Заголовок діалогу події"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                background: transparent;
                border: none;
                margin-bottom: 15px;
            }}
        """



    @staticmethod
    def events_card():
        """Картка з подіями"""
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 20px;
                margin: 12px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                line-height: 1.5;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def reminder_section():
        """Секція нагадувань в діалозі"""
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(139, 92, 246, 0.1), 
                    stop:1 rgba(236, 72, 153, 0.1));
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 16px;
            }}
        """

    @staticmethod
    def reminder_checkbox():
        """Чекбокс нагадування"""
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 600;
                spacing: 12px;
                background: transparent;
                border: none;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 8px;
                border: 2px solid rgba(139, 92, 246, 0.5);
                background: rgba(255, 255, 255, 0.1);
            }}
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #8B5CF6, stop:1 #EC4899);
                border: 2px solid #8B5CF6;
            }}
        """

    @staticmethod
    def event_dialog_reminder_frame():
        """Фрейм для секції нагадувань (без додаткової рамки)"""
        return f"""
            QFrame {{
                background: transparent;
                border: none;
                border-radius: 0px;
            }}
        """

    @staticmethod
    def event_dialog_reminder_checkbox():
        """Чекбокс нагадування в діалозі"""
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 15px;
                font-weight: 600;
                spacing: 12px;
                background: transparent;
                border: none;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 8px;
                border: 2px solid rgba(139, 92, 246, 0.5);
                background: rgba(255, 255, 255, 0.1);
            }}
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #8B5CF6, stop:1 #EC4899);
                border: 2px solid #8B5CF6;
            }}
        """

    @staticmethod
    def event_dialog_field_label():
        """Підписи полів в діалозі"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-weight: 500;
                margin-top: 10px;
                background: transparent;
                border: none;
            }}
        """

    @staticmethod
    def event_dialog_hint_label():
        """Підказки в діалозі"""
        return f"""
            QLabel {{
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
                margin-top: 5px;
                background: transparent;
                border: none;
            }}
        """