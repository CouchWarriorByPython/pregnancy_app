"""
Стилі для екранів авторизації
"""

from .base import Colors


class AuthStyles:
    @staticmethod
    def main_container():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def title_label():
        return f"""
            QLabel {{
                color: {Colors.TEXT_ACCENT};
                font-size: 24px;
                font-weight: bold;
                text-align: center;
            }}
        """

    @staticmethod
    def subtitle_label():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                text-align: center;
            }}
        """

    @staticmethod
    def auth_input():
        return f"""
            QLineEdit {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 8px;
                padding: 15px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def auth_button_large():
        return f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-weight: bold;
                font-size: 16px;
                min-height: 25px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRIMARY_PRESSED};
            }}
        """

    @staticmethod
    def switch_button():
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {Colors.PRIMARY};
                color: {Colors.PRIMARY};
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 140, 0, 0.2);
            }}
        """

    @staticmethod
    def verification_code_input():
        return f"""
            QLineEdit {{
                background-color: {Colors.SURFACE_VARIANT};
                border: 2px solid {Colors.BORDER};
                border-radius: 10px;
                padding: 15px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: bold;
                letter-spacing: 5px;
                text-align: center;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def resend_button():
        return f"""
            QPushButton {{
                background-color: {Colors.SURFACE_VARIANT};
                color: {Colors.TEXT_PRIMARY};
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.BORDER_HOVER};
            }}
        """

    @staticmethod
    def back_button():
        return f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.TEXT_SECONDARY};
                border-radius: 8px;
                padding: 10px;
            }}
            QPushButton:hover {{
                color: {Colors.TEXT_PRIMARY};
                border-color: {Colors.TEXT_PRIMARY};
            }}
        """


class LoginStyles(AuthStyles):
    @staticmethod
    def login_form():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
                border-radius: 20px;
                padding: 20px;
            }}
        """

    @staticmethod
    def forgot_password_link():
        return f"""
            QLabel {{
                color: {Colors.PRIMARY};
                text-decoration: underline;
            }}
            QLabel:hover {{
                color: {Colors.PRIMARY_HOVER};
            }}
        """


class RegisterStyles(AuthStyles):
    @staticmethod
    def register_form():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
                border-radius: 20px;
                padding: 20px;
            }}
        """

    @staticmethod
    def password_strength_indicator():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 12px;
                padding: 5px;
            }}
        """


class VerificationStyles(AuthStyles):
    @staticmethod
    def verification_form():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
                border-radius: 20px;
                padding: 20px;
            }}
        """

    @staticmethod
    def code_description():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                text-align: center;
                line-height: 1.4;
            }}
        """

    @staticmethod
    def timer_label():
        return f"""
            QLabel {{
                color: {Colors.WARNING};
                font-size: 12px;
                text-align: center;
            }}
        """