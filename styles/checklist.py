"""
Стилі для екрану чекліста
"""

from .base import Colors


class ChecklistStyles:
    @staticmethod
    def tab_button():
        return f"""
            QPushButton {{
                background: rgba(255, 255, 255, 0.05);
                color: {Colors.TEXT_SECONDARY};
                border: none;
                font-size: 14px;
                font-weight: 500;
                padding: 16px 24px;
                text-align: center;
                border-radius: 12px;
                margin: 4px;
            }}
            QPushButton:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                font-weight: 700;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }}
            QPushButton:hover:!checked {{
                background: rgba(255, 255, 255, 0.1);
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def progress_bar():
        return f"""
            QLabel {{
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 4px;
                text-align: center;
                color: white;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
        """

    @staticmethod
    def progress_bar_dynamic(progress_percent):
        return f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.PRIMARY}, stop:{progress_percent / 100} {Colors.SECONDARY},
                    stop:{progress_percent / 100} rgba(255, 255, 255, 0.1), stop:1 rgba(255, 255, 255, 0.1));
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 4px;
                text-align: center;
                color: white;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
        """

    @staticmethod
    def section_title():
        return f"""
            font-family: 'Segoe UI', Arial; 
            font-size: 18px; 
            font-weight: 700;
            color: {Colors.TEXT_ACCENT};
            margin: 16px 0 12px 0;
        """

    @staticmethod
    def checklist_frame():
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 20px;
                margin: 12px;
            }}
        """

    @staticmethod
    def check_item():
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                font-weight: 500;
                spacing: 12px;
                padding: 8px;
                border-radius: 8px;
                margin: 2px 0;
            }}
            QCheckBox:hover {{
                background: rgba(255, 255, 255, 0.05);
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 8px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 2px solid {Colors.PRIMARY};
            }}
        """