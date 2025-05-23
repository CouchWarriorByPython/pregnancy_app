"""
Стилі для екранів онбордингу
"""

from .base import Colors


class OnboardingStyles:
    @staticmethod
    def main_container():
        return f"""
            QWidget {{
                background: {Colors.BACKGROUND_GRADIENT};
                color: {Colors.TEXT_PRIMARY};
            }}
        """

    @staticmethod
    def step_title():
        return f"""
            QLabel {{
                color: white;
                font-size: 26px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 20px;
            }}
        """

    @staticmethod
    def step_subtitle():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 16px;
                font-weight: 500;
                text-align: center;
                margin-bottom: 30px;
                line-height: 1.5;
            }}
        """

    @staticmethod
    def form_section():
        return f"""
            QWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 24px;
                margin: 12px;
            }}
        """

    @staticmethod
    def section_label():
        return f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 16px;
            }}
        """

    @staticmethod
    def field_label():
        return f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
            }}
        """

    @staticmethod
    def onboarding_input():
        return f"""
            QLineEdit {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 16px 20px;
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
    def onboarding_button():
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
    def back_button():
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
    def progress_indicator():
        return f"""
            QWidget {{
                background: {Colors.GLASS_SURFACE};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 20px;
                padding: 16px;
            }}
        """

    @staticmethod
    def progress_step_active():
        return f"""
            QLabel {{
                background: {Colors.PRIMARY_GRADIENT};
                color: white;
                border-radius: 16px;
                padding: 12px 16px;
                font-weight: 700;
                text-align: center;
                font-size: 14px;
            }}
        """

    @staticmethod
    def progress_step_inactive():
        return f"""
            QLabel {{
                background: rgba(255, 255, 255, 0.1);
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: 16px;
                padding: 12px 16px;
                font-weight: 500;
                text-align: center;
                font-size: 14px;
            }}
        """


class ChildInfoStyles(OnboardingStyles):
    @staticmethod
    def gender_section():
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(236, 72, 153, 0.1), stop:1 rgba(219, 39, 119, 0.05));
                border: 1px solid rgba(236, 72, 153, 0.3);
                border-radius: 20px;
                padding: 24px;
                margin: 12px 0;
            }}
        """

    @staticmethod
    def gender_radio():
        return f"""
            QRadioButton {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                padding: 16px;
                spacing: 16px;
                border-radius: 12px;
                margin: 4px 0;
            }}
            QRadioButton:hover {{
                background: rgba(255, 255, 255, 0.05);
            }}
            QRadioButton::indicator {{
                width: 28px;
                height: 28px;
                border-radius: 14px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QRadioButton::indicator:checked {{
                background: {Colors.PRIMARY_GRADIENT};
                border: 3px solid white;
            }}
        """

    @staticmethod
    def first_labour_checkbox():
        return f"""
            QCheckBox {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: 600;
                padding: 20px;
                spacing: 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(16, 185, 129, 0.1), stop:1 rgba(5, 150, 105, 0.05));
                border: 1px solid rgba(16, 185, 129, 0.3);
                border-radius: 16px;
                margin: 12px 0;
            }}
            QCheckBox:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(16, 185, 129, 0.15), stop:1 rgba(5, 150, 105, 0.1));
            }}
            QCheckBox::indicator {{
                width: 28px;
                height: 28px;
                border-radius: 8px;
                border: 2px solid {Colors.GLASS_BORDER};
                background: {Colors.GLASS_SURFACE};
            }}
            QCheckBox::indicator:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #10B981, stop:1 #059669);
                border: 3px solid white;
            }}
        """