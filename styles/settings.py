"""
Стилі для екрану налаштувань
"""

from .base import BaseStyles, Colors


class SettingsStyles:
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
                transform: scale(1.02);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }}
            QPushButton:hover:!checked {{
                background: rgba(255, 255, 255, 0.1);
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def logout_section():
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(239, 68, 68, 0.1), stop:1 rgba(220, 38, 38, 0.05));
                border-top: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: 16px;
                margin: 8px;
                backdrop-filter: blur(10px);
            }}
        """

    @staticmethod
    def editor_form():
        return f"""
            QFrame {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 24px;
                margin: 12px;
                backdrop-filter: blur(15px);
            }}
        """

    @staticmethod
    def info_frame():
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(59, 130, 246, 0.1), stop:1 rgba(29, 78, 216, 0.05));
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 20px;
                padding: 20px;
                margin: 12px;
                backdrop-filter: blur(15px);
            }}
        """

    @staticmethod
    def save_button():
        return BaseStyles.button_primary()

    @staticmethod
    def logout_button():
        return BaseStyles.button_error()