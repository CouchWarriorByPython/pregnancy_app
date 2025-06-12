"""
Стилі для екранів авторизації
"""

from ..base import Colors


class AuthScreenStyles:
    @staticmethod
    def main_container():
        """Основний контейнер для всіх екранів авторизації"""
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def title_label():
        """Заголовок екранів авторизації"""
        return f"""
            QLabel {{
                color: white;
                font-size: 28px;
                font-weight: 700;
                text-align: center;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def subtitle_label():
        """Підзаголовок екранів авторизації"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
                font-weight: 500;
                text-align: center;
                line-height: 1.4;
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }}
        """

    @staticmethod
    def auth_input():
        """Поля введення для авторизації"""
        return f"""
            QLineEdit {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 18px 24px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 500;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
                background: rgba(255, 255, 255, 0.12);
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_SECONDARY};
                font-weight: 400;
            }}
        """

    @staticmethod
    def auth_button_large():
        """Великі кнопки авторизації"""
        return f"""
            QPushButton {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 18px 32px;
                font-weight: 700;
                font-size: 16px;
                min-height: 20px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #7C3AED, stop:1 #DB2777);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6D28D9, stop:1 #BE185D);
            }}
        """

    @staticmethod
    def switch_button():
        """Кнопки перемикання між екранами"""
        return f"""
            QPushButton {{
                background: transparent;
                border: 2px solid {Colors.PRIMARY};
                color: {Colors.PRIMARY};
                border-radius: 16px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: rgba(139, 92, 246, 0.1);
                border: 2px solid {Colors.PRIMARY_HOVER};
                color: white;
            }}
        """

    @staticmethod
    def verification_code_input():
        """Поле для коду підтвердження"""
        return f"""
            QLineEdit {{
                background: {Colors.GLASS_SURFACE};
                border: 2px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 20px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 24px;
                font-weight: 700;
                letter-spacing: 8px;
                text-align: center;
                min-height: 20px;
            }}
            QLineEdit:focus {{
                border: 3px solid {Colors.PRIMARY};
                background: rgba(255, 255, 255, 0.15);
            }}
        """

    @staticmethod
    def code_description():
        """Опис коду підтвердження"""
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
                font-weight: 500;
                text-align: center;
                line-height: 1.5;
                margin: 16px 0;
                background: transparent;
                border: none;
                padding: 0px;
            }}
        """

    @staticmethod
    def resend_button():
        """Кнопка повторного надсилання"""
        return f"""
            QPushButton {{
                background: {Colors.SURFACE};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 14px 24px;
                font-weight: 600;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: {Colors.SURFACE_HOVER};
                border: 1px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def back_button():
        """Кнопка назад"""
        return f"""
            QPushButton {{
                background: transparent;
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.TEXT_SECONDARY};
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: 500;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {Colors.TEXT_PRIMARY};
                border-color: {Colors.TEXT_PRIMARY};
                background: rgba(255, 255, 255, 0.05);
            }}
        """