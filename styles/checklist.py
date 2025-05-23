"""
Стилі для екрану чекліста
"""

from .base import Colors


class ChecklistStyles:
    @staticmethod
    def tab_button():
        return f"""
            QPushButton {{
                background-color: {Colors.BACKGROUND};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                font-size: 14px;
                padding: 10px;
                text-align: center;
            }}
            QPushButton:checked {{
                background-color: {Colors.SURFACE};
                color: {Colors.PRIMARY};
                font-weight: bold;
            }}
            QPushButton:hover:!checked {{
                background-color: #1A1A1A;
            }}
        """

    @staticmethod
    def progress_bar():
        return f"""
            QLabel {{
                background-color: {Colors.SURFACE_VARIANT};
                border-radius: 10px;
                padding: 0px;
                text-align: left;
            }}
        """

    @staticmethod
    def progress_bar_dynamic(progress_percent):
        return f"""
            QLabel {{
                background-color: {Colors.SURFACE_VARIANT};
                border-radius: 10px;
                padding: 0px;
                text-align: left;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.PRIMARY}, stop:{progress_percent / 100} {Colors.PRIMARY},
                    stop:{progress_percent / 100} {Colors.SURFACE_VARIANT}, stop:1 {Colors.SURFACE_VARIANT});
            }}
        """

    @staticmethod
    def section_title():
        return "font-family: Arial; font-size: 16px; font-weight: bold;"

    @staticmethod
    def checklist_frame():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 10px;
            }}
        """

    @staticmethod
    def check_item():
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid {Colors.BORDER};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.SUCCESS};
                border: 2px solid {Colors.SUCCESS};
            }}
        """