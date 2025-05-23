"""
Стилі для екрану налаштувань
"""

from .base import BaseStyles, Colors


class SettingsStyles:
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
    def logout_section():
        return """
            QWidget {
                background-color: #1a1a1a;
                border-top: 1px solid #333;
            }
        """

    @staticmethod
    def editor_form():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 15px;
            }}
        """

    @staticmethod
    def info_frame():
        return f"""
            QFrame {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 15px;
            }}
        """

    @staticmethod
    def save_button():
        return BaseStyles.button_primary()

    @staticmethod
    def logout_button():
        return BaseStyles.button_error()