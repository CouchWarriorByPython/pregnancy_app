"""
Стилі для екрану календаря
"""

from .base import Colors


class CalendarStyles:
    @staticmethod
    def calendar_widget():
        return f"""
            QCalendarWidget {{
                background-color: {Colors.BACKGROUND};
            }}
            QCalendarWidget QToolButton {{
                color: {Colors.TEXT_PRIMARY};
                background-color: {Colors.SURFACE_VARIANT};
                border-radius: 5px;
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                color: {Colors.TEXT_PRIMARY};
                background-color: {Colors.BACKGROUND};
                selection-background-color: {Colors.PRIMARY};
                selection-color: white;
            }}
        """

    @staticmethod
    def event_dialog():
        return f"""
            QDialog {{
                background-color: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def events_card():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
        """