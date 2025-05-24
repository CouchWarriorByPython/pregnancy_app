"""
Стилі для екрану календаря
"""

from .base import Colors


class CalendarStyles:
    @staticmethod
    def calendar_widget():
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
        return f"""
            QDialog {{
                background: {Colors.BACKGROUND_GRADIENT};
                color: {Colors.TEXT_PRIMARY};
                border-radius: 20px;
                border: 1px solid {Colors.GLASS_BORDER};
            }}
        """

    @staticmethod
    def events_card():
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
            }}
        """