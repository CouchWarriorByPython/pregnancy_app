"""
Стилі для екранів онбордингу
"""

from .base import Colors


class OnboardingStyles:
    @staticmethod
    def main_container():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def step_title():
        return f"""
            QLabel {{
                color: {Colors.TEXT_ACCENT};
                font-size: 22px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }}
        """

    @staticmethod
    def step_subtitle():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                text-align: center;
                margin-bottom: 30px;
            }}
        """

    @staticmethod
    def form_section():
        return f"""
            QWidget {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
            }}
        """

    @staticmethod
    def section_label():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
        """

    @staticmethod
    def field_label():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                margin-bottom: 5px;
            }}
        """

    @staticmethod
    def onboarding_input():
        return f"""
            QLineEdit {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 25px;
            }}
            QLineEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def onboarding_button():
        return f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                font-weight: bold;
                font-size: 16px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRIMARY_PRESSED};
            }}
        """

    @staticmethod
    def back_button():
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
    def progress_indicator():
        return f"""
            QWidget {{
                background-color: {Colors.SURFACE};
                border-radius: 20px;
                padding: 10px;
            }}
        """

    @staticmethod
    def progress_step_active():
        return f"""
            QLabel {{
                background-color: {Colors.PRIMARY};
                color: white;
                border-radius: 15px;
                padding: 8px;
                font-weight: bold;
                text-align: center;
            }}
        """

    @staticmethod
    def progress_step_inactive():
        return f"""
            QLabel {{
                background-color: {Colors.SURFACE_VARIANT};
                color: {Colors.TEXT_SECONDARY};
                border-radius: 15px;
                padding: 8px;
                text-align: center;
            }}
        """


class ChildInfoStyles(OnboardingStyles):
    @staticmethod
    def gender_section():
        return f"""
            QWidget {{
                background-color: {Colors.SURFACE};
                border-radius: 15px;
                padding: 20px;
                margin: 10px 0;
            }}
        """

    @staticmethod
    def gender_radio():
        return f"""
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                padding: 10px;
                spacing: 10px;
            }}
            QRadioButton::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 12px;
                border: 2px solid {Colors.BORDER};
            }}
            QRadioButton::indicator:checked {{
                background-color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def first_labour_checkbox():
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                padding: 15px;
                spacing: 10px;
            }}
            QCheckBox::indicator {{
                width: 24px;
                height: 24px;
                border-radius: 4px;
                border: 2px solid {Colors.BORDER};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.SUCCESS};
                border: 2px solid {Colors.SUCCESS};
            }}
        """


class UserInfoStyles(OnboardingStyles):
    @staticmethod
    def form_layout():
        return f"""
            QFormLayout {{
                spacing: 15px;
            }}
        """

    @staticmethod
    def spinbox_input():
        return f"""
            QSpinBox, QDoubleSpinBox {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 25px;
            }}
            QSpinBox:focus, QDoubleSpinBox:focus {{
                border: 2px solid {Colors.PRIMARY};
            }}
        """

    @staticmethod
    def date_input():
        return f"""
            QDateEdit {{
                background-color: {Colors.SURFACE_VARIANT};
                border: none;
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
                min-height: 25px;
            }}
            QDateEdit:focus {{
                border: 2px solid {Colors.PRIMARY};
            }}
        """


class PregnancyInfoStyles(OnboardingStyles):
    @staticmethod
    def date_form():
        return f"""
            QFormLayout {{
                spacing: 20px;
                padding: 20px;
            }}
        """

    @staticmethod
    def info_note():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 13px;
                font-style: italic;
                padding: 10px;
                background-color: {Colors.SURFACE_VARIANT};
                border-radius: 8px;
            }}
        """

    @staticmethod
    def due_date_display():
        return f"""
            QLabel {{
                color: {Colors.SUCCESS};
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
                background-color: {Colors.SURFACE};
                border-radius: 10px;
                border: 2px solid {Colors.SUCCESS};
            }}
        """

    @staticmethod
    def calculation_method():
        return f"""
            QWidget {{
                background-color: {Colors.SURFACE};
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            }}
        """


class WelcomeStyles(OnboardingStyles):
    @staticmethod
    def welcome_container():
        return f"""
            QWidget {{
                background-color: {Colors.BACKGROUND};
                padding: 40px;
            }}
        """

    @staticmethod
    def app_title():
        return f"""
            QLabel {{
                color: {Colors.TEXT_ACCENT};
                font-size: 28px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }}
        """

    @staticmethod
    def welcome_text():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                text-align: center;
                line-height: 1.5;
                margin-bottom: 40px;
            }}
        """

    @staticmethod
    def feature_list():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                padding: 20px;
                background-color: {Colors.SURFACE};
                border-radius: 10px;
                margin: 20px 0;
            }}
        """

    @staticmethod
    def start_button():
        return f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 20px;
                padding: 20px;
                font-weight: bold;
                font-size: 18px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_HOVER};
            }}
        """

    @staticmethod
    def login_button():
        return f"""
            QPushButton {{
                background-color: transparent;
                border: 2px solid {Colors.PRIMARY};
                color: {Colors.PRIMARY};
                border-radius: 15px;
                padding: 15px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 140, 0, 0.2);
            }}
        """